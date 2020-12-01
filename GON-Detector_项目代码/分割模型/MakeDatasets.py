from models import DeepModel
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf;
from PIL import Image
import numpy as np
from skimage.measure import label,regionprops
from skimage.transform import rotate
from tools import BW_img,disc_crop,enhance_img
import os

#some hyper parameters
Disc_ROI=600
Unet_size=640

#init my unet model
unet_weights_url='model_weights/Model_DiscSeg_ORIGA.h5'
my_unet_model=DeepModel(Unet_size)
my_unet_model.load_weights(unet_weights_url)

#build my dataset

img_path='G:\\glaucoma\\val_img\\'
label_path='G:\\glaucoma\\mask\\'
img_save_path='E:\\GON-datasets\\valid-images\\'
label_save_path='E:\\GON-datasets\\labels\\'

#build img_list.txt
def WriteTxtFile(dir):
    writer=open('img_list.txt','w')
    for file in os.listdir(dir):
        name=file[:-4]
        writer.write(name+'\n')
    writer.close()

WriteTxtFile(img_path)
file=open('img_list.txt','r')

lines=file.readlines()
for line in lines:
    line=line[:-1]
    #get path
    path1=img_path+line+".jpg"
    path2=label_path+line+".bmp"

    old_img=Image.open(path1)
    old_label=Image.open(path2)
    org_img=np.array(old_img)
    label_img=np.array(old_label)
    new_label=np.zeros(label_img.shape+(3,),dtype=np.uint8)
    new_label[label_img<200,0]=255
    new_label[label_img<100,1]=255

    #main algorithm
    test_img=old_img.resize((Unet_size,Unet_size))
    test_img=np.array(test_img)
    test_img=np.reshape(test_img,(1,)+test_img.shape)
    disc_map=my_unet_model.predict([test_img])
    disc_map=BW_img(np.reshape(disc_map,(Unet_size,Unet_size)),0.5)
    regions = regionprops(label(disc_map))

    #orginal coordinate
    C_x = int(regions[0].centroid[0] * org_img.shape[0] / 640)
    C_y = int(regions[0].centroid[1] * org_img.shape[1] / 640)

    #crop img and label and PT,both ndarray are (600,600,3)
    disc_region, err_coord, crop_coord = disc_crop(org_img, Disc_ROI, C_x, C_y)
    label_region, _, _ = disc_crop(new_label, Disc_ROI, C_x, C_y)

    #clahe algorithm
    clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    R,G,B=cv2.split(disc_region)
    new_R=clahe.apply(R)
    new_G=clahe.apply(G)
    new_B=clahe.apply(B)
    disc_region=cv2.merge((new_R,new_G,new_B))

    #transform the dataset
    disc_Image=Image.fromarray(disc_region.astype(np.uint8))
    label_Image=Image.fromarray(label_region.astype(np.uint8))
    disc_dataset=enhance_img(disc_Image)
    label_dataset=enhance_img(label_Image)
    for i in range(6):
        Disc_flat = rotate(cv2.linearPolar(disc_dataset[i], (Disc_ROI / 2, Disc_ROI / 2), Disc_ROI / 2,
                                           cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS), -90)
        Label_flat = rotate(cv2.linearPolar(label_dataset[i], (Disc_ROI / 2, Disc_ROI / 2), Disc_ROI / 2,
                                            cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS), -90)
        disc_result = Image.fromarray((Disc_flat * 255).astype(np.uint8))
        label_result = Image.fromarray((Label_flat * 255).astype(np.uint8))
        label_result.save(label_save_path + line + '_' +str(i) +'.png')
        disc_result.save(img_save_path + line + '_' + str(i) +'.png')




    '''
    Disc_flat = rotate(cv2.linearPolar(disc_region, (Disc_ROI / 2, Disc_ROI / 2), Disc_ROI / 2,
                                       cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS), -90)
    Label_flat = rotate(cv2.linearPolar(label_region, (Disc_ROI / 2, Disc_ROI / 2), Disc_ROI / 2,
                                        cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS), -90)

    #save the image and label
    disc_result = Image.fromarray((Disc_flat * 255).astype(np.uint8))
    label_result = Image.fromarray((Label_flat * 255).astype(np.uint8))
    save_name = '{}.png'.format(line)
    label_result.save(label_save_path+save_name)
    disc_result.save(img_save_path+save_name)
    #disc_result.show()
    #label_result.show()
    '''
file.close()


'''
test_img=Image.open('test_img/V0001.jpg')
test_img=test_img.resize((640,640))
test_img=np.array(test_img)
test_img=np.reshape(test_img,(1,)+test_img.shape)

disc_map=my_unet_model.predict([test_img])
print(disc_map.shape)
'''