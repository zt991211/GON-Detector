from PIL import Image,ImageEnhance
import numpy as np
from scipy.ndimage import binary_fill_holes
import cv2
import os
from skimage.measure import label,regionprops
from tensorflow.keras import backend as K


def cal(img):
    height=img.shape[0]
    width=img.shape[1]
    h_first=0
    h_end=0
    w_first=0
    w_end=0
    for i in range(height-1):
        if sum(img[i,:])>255:
            h_first=i
            break
    for i in range(height-1):
        if sum(img[i,:])>255:
            h_end=i
    h=abs(h_first-h_end)
    for i in range(width-1):
        if sum(img[:,i])>255:
            w_first=i
            break
    for i in range(width-1):
        if sum(img[:,i])>255:
            w_end=i
    w=abs(w_first-w_end)
    return [h,w]

def pro_process(temp_img, input_size):
    img = np.asarray(temp_img).astype('float32')
    img = np.array(Image.fromarray(img, mode='RGB').resize((input_size, input_size)))
    return img

#load my dataset
def getDataSet(data_path, data_type):
    data_list = []
    for file in os.listdir(data_path):
        if file.lower().endswith(data_type):
            img=Image.open(data_path+file)
            img=np.array(img)
            data_list.append(img)
    return data_list

def dice_coef(y_true, y_pred):
    smooth=1.
    y_true_f = K.flatten(y_true) # 将 y_true 拉伸为一维.
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f * y_true_f) + K.sum(y_pred_f * y_pred_f) + smooth)

def dice_coef2(y_true, y_pred):
    score0 = dice_coef(y_true[:, :, :, 0], y_pred[:, :, :, 0])
    score1 = dice_coef(y_true[:, :, :, 1], y_pred[:, :, :, 1])
    score = 0.5 * score0 + 0.5 * score1
    return score

def dice_coef_loss(y_true, y_pred):
    return 1.-dice_coef2(y_true, y_pred)



def BW_img(input, thresholding):

    if input.max() > thresholding:
        binary = input > thresholding
    else:
        binary = input > input.max() / 2.0

    label_image = label(binary)
    regions = regionprops(label_image)
    area_list = [region.area for region in regions]
    if area_list:
        idx_max = np.argmax(area_list)
        binary[label_image != idx_max + 1] = 0
    return binary_fill_holes(np.asarray(binary).astype(int))

def disc_crop(org_img, DiscROI_size, C_x, C_y):
    tmp_size = int(DiscROI_size / 2)
    disc_region = np.zeros((DiscROI_size, DiscROI_size, 3), dtype=org_img.dtype)
    crop_coord = np.array([C_x - tmp_size, C_x + tmp_size, C_y - tmp_size, C_y + tmp_size], dtype=int)
    err_coord = [0, DiscROI_size, 0, DiscROI_size]

    if crop_coord[0] < 0:
        err_coord[0] = abs(crop_coord[0])
        crop_coord[0] = 0

    if crop_coord[2] < 0:
        err_coord[2] = abs(crop_coord[2])
        crop_coord[2] = 0

    if crop_coord[1] > org_img.shape[0]:
        err_coord[1] = err_coord[1] - (crop_coord[1] - org_img.shape[0])
        crop_coord[1] = org_img.shape[0]

    if crop_coord[3] > org_img.shape[1]:
        err_coord[3] = err_coord[3] - (crop_coord[3] - org_img.shape[1])
        crop_coord[3] = org_img.shape[1]

    disc_region[err_coord[0]:err_coord[1], err_coord[2]:err_coord[3], ] = org_img[
                                                                          crop_coord[0]:crop_coord[1],
                                                                          crop_coord[2]:crop_coord[3],
                                                                          ]

    return disc_region, err_coord, crop_coord

def enhance_img(org_PIL_img):
    r90=np.array(org_PIL_img.rotate(90))
    r180=np.array(org_PIL_img.rotate(180))
    r270=np.array(org_PIL_img.rotate(270))
    imgc=np.array(ImageEnhance.Color(org_PIL_img).enhance(1.5))
    imgs=np.array(ImageEnhance.Sharpness(org_PIL_img).enhance(1.5))
    list=[np.array(org_PIL_img),r90,r180,r270,imgc,imgs]
    return list
