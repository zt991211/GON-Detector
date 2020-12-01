from flask import Flask,request,jsonify,make_response
from Unet import DeepModel
from Mnet import M_net
from paddle import fluid
import cv2,os,json
from PIL import Image
import numpy as np
from skimage.measure import label,regionprops
from tools import BW_img,disc_crop,getCDR,transform_img,base64_to_pil,test_transform
from skimage.transform import rotate, resize
from flask_cors import CORS
import torch
import torch.nn.functional as F
import torch.nn as nn
from torchvision import transforms,models
from io import BytesIO


app = Flask(__name__)
CORS(app, supports_credentials=True)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
classes=['0','1']


@app.route('/')
def hello_world():
    return 'Hello World!'

basedir='/www/wwwroot/gondetector.cn/php/userdata/'
Disc_ROI=600
DiscROI_size=600
Unet_size=640
Unet_weights='weights/Model_DiscSeg_ORIGA.h5'
Unet_model=DeepModel(Unet_size)
Unet_model.load_weights(Unet_weights)


# /root/.cache/pytorch/
V3_model = models.inception_v3(pretrained=True,aux_logits = False)
for params in V3_model.parameters():
    params.require_grad = False
fc = nn.Sequential(
    nn.Linear(2048,1024),
    nn.ReLU(),
    nn.Linear(1024,2)
)
V3_model.fc = fc
state_dict = torch.load("weights/gondetector-2.pth")
V3_model.load_state_dict(state_dict)


def get_ROI_region(img):
    old_img = img
    org_img = np.array(old_img)
    test_img = old_img.resize((Unet_size, Unet_size))
    test_img = np.array(test_img)
    test_img = np.reshape(test_img, (1,) + test_img.shape)
    disc_map = Unet_model.predict([test_img])
    disc_map = BW_img(np.reshape(disc_map, (Unet_size, Unet_size)), 0.5)
    regions = regionprops(label(disc_map))
    # orginal coordinate
    C_x = int(regions[0].centroid[0] * org_img.shape[0] / 640)
    C_y = int(regions[0].centroid[1] * org_img.shape[1] / 640)
    # crop img and label and PT,both ndarray are (600,600,3)
    disc_region, err_coord, crop_coord = disc_crop(org_img, Disc_ROI, C_x, C_y)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    R, G, B = cv2.split(disc_region)
    new_R = clahe.apply(R)
    new_G = clahe.apply(G)
    new_B = clahe.apply(B)
    disc_region = cv2.merge((new_R, new_G, new_B))
    disc_Image = Image.fromarray(disc_region.astype(np.uint8))
    Disc_flat = rotate(cv2.linearPolar(disc_region, (Disc_ROI / 2, Disc_ROI / 2), Disc_ROI / 2,
                                       cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS), -90)
    disc_result = Image.fromarray((Disc_flat * 255).astype(np.uint8))
    return disc_Image,disc_result


@app.route('/uploader',methods=['POST','GET'])
def uploadImage():
    print('success')
    img=request.files['photo']
    #转换二进制图片格式到PIL
    #code below
    print(type(img))
    #img=Image.open(BytesIO(img))
    #print(type(img))
    print(img.filename)
    save_dir='./test_img/'+img.filename
    #number_id=len(os.listdir('./test_img'))+1
    #save image
    #code below
    img.save(save_dir)
    return str(img.filename)


@app.route('/CDRpredict/<usrname>/<imgname>')
def prediction(usrname,imgname):
    path=basedir+usrname+'/picture/'+imgname
    img1=Image.open(path)
    org_ROI,ROI_PT=get_ROI_region(img1)
    img = []
    img.append(transform_img(np.array(ROI_PT)))
    img = np.array(img).astype('float32')
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    in_var = img
    program, feed_vars, fetch_vars = fluid.io.load_inference_model('weights/mnet_model/home/aistudio/work/mnet_model',
                                                                   executor=exe)
    fetch = exe.run(program, feed={feed_vars[0]: in_var}, fetch_list=fetch_vars)
    out10 = fetch[4]
    out10 = np.reshape(out10, (out10.shape[1], out10.shape[2], out10.shape[3]))
    out10 = np.transpose(out10, (1, 2, 0))
    disc_map = np.array(Image.fromarray(out10[:, :, 0]).resize((600, 600)))
    cup_map = np.array(Image.fromarray(out10[:, :, 1]).resize((600, 600)))
    disc_map[-round(DiscROI_size / 3):, :] = 0
    cup_map[-round(DiscROI_size / 2):, :] = 0
    De_disc_map = cv2.linearPolar(rotate(disc_map, 90), (DiscROI_size / 2, DiscROI_size / 2),
                                  DiscROI_size / 2, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)
    De_cup_map = cv2.linearPolar(rotate(cup_map, 90), (DiscROI_size / 2, DiscROI_size / 2),
                                 DiscROI_size / 2, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)
    ret, De_cup_map = cv2.threshold(De_cup_map, 0.5, 1, cv2.THRESH_BINARY)
    res, De_disc_map = cv2.threshold(De_disc_map, 0.5, 1, cv2.THRESH_BINARY)
    disc_h, disc_w = getCDR(De_disc_map)
    cup_h, cup_w = getCDR(De_cup_map)
    V_cdr=cup_h * 1.00 / disc_h
    W_cdr=cup_w * 1.00/ disc_w
    return_info={}
    return_info['VCDR']=V_cdr
    return_info['HCDR']=W_cdr
    return jsonify(return_info)
    #res=make_response(jsonify({"VCDR":str(V_cdr), "WCDR":str(W_cdr)}))
    #res.headers['Access-Control-Allow-Origin'] = '*'
    #return res


@app.route('/V3predict/<usrname>/<imgname>')
def predict_image(usrname,imgname):
    V3_model.eval()
    image_path=basedir+usrname+'/picture/'+imgname
    img = Image.open(image_path)
    img_tensor = test_transform(img)
    img_tensor = torch.stack([img_tensor])
    output = V3_model(img_tensor)
    _,preds = torch.max(output,dim=1)
    return_info={}
    return_info['PROB']=torch.softmax(output,dim=1)[:,1].item()*100
    return jsonify(return_info)
    #print('prob:{}%'.format(torch.max(torch.softmax(output,dim=1)).item()*100))


@app.route('/vx/<imgname>')
def vx_predict(imgname):
    return_info={}
    path='./test_img/'+imgname
    img1=Image.open(path)
    org_ROI,ROI_PT=get_ROI_region(img1)
    img = []
    img.append(transform_img(np.array(ROI_PT)))
    img = np.array(img).astype('float32')
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    in_var = img
    program, feed_vars, fetch_vars = fluid.io.load_inference_model('weights/mnet_model/home/aistudio/work/mnet_model',
                                                                   executor=exe)
    fetch = exe.run(program, feed={feed_vars[0]: in_var}, fetch_list=fetch_vars)
    out10 = fetch[4]
    out10 = np.reshape(out10, (out10.shape[1], out10.shape[2], out10.shape[3]))
    out10 = np.transpose(out10, (1, 2, 0))
    disc_map = np.array(Image.fromarray(out10[:, :, 0]).resize((600, 600)))
    cup_map = np.array(Image.fromarray(out10[:, :, 1]).resize((600, 600)))
    disc_map[-round(DiscROI_size / 3):, :] = 0
    cup_map[-round(DiscROI_size / 2):, :] = 0
    De_disc_map = cv2.linearPolar(rotate(disc_map, 90), (DiscROI_size / 2, DiscROI_size / 2),
                                  DiscROI_size / 2, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)
    De_cup_map = cv2.linearPolar(rotate(cup_map, 90), (DiscROI_size / 2, DiscROI_size / 2),
                                 DiscROI_size / 2, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)
    ret, De_cup_map = cv2.threshold(De_cup_map, 0.5, 1, cv2.THRESH_BINARY)
    res, De_disc_map = cv2.threshold(De_disc_map, 0.5, 1, cv2.THRESH_BINARY)
    disc_h, disc_w = getCDR(De_disc_map)
    cup_h, cup_w = getCDR(De_cup_map)
    V_cdr=cup_h * 1.00 / disc_h
    W_cdr=cup_w * 1.00/ disc_w
    return_info['VCDR']=V_cdr
    return_info['HCDR']=W_cdr
    V3_model.eval()
    image_path='./test_img/'+imgname
    img = Image.open(image_path)
    img_tensor = test_transform(img)
    img_tensor = torch.stack([img_tensor])
    output = V3_model(img_tensor)
    _,preds = torch.max(output,dim=1)
    return_info['PROB']=torch.softmax(output,dim=1)[:,1].item()*100
    return jsonify(return_info)
