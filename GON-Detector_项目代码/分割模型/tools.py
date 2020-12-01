import numpy as np
from scipy.ndimage import binary_fill_holes
from skimage.measure import label,regionprops
import cv2
import re
from PIL import Image
import base64
from io import BytesIO

def base64_to_pil(img_base64):
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image


def getCDR(img):
    height = img.shape[0]
    width = img.shape[1]
    h_first = 0
    h_end = 0
    w_first = 0
    w_end = 0
    for i in range(height):
        if sum(img[i, :]) >= 1:
            h_first = i
            break
    for i in range(height):
        if sum(img[i, :]) >= 1:
            h_end = i
    h = abs(h_first - h_end)
    for i in range(width):
        if sum(img[:, i]) >= 1:
            w_first = i
            break
    for i in range(width):
        if sum(img[:, i]) >= 1:
            w_end = i
    w = abs(w_first - w_end)
    return h, w


# 对读入的图像数据进行预处理
def transform_img(img, flag=0):
    # 将图片尺寸缩放道 400*400
    img = cv2.resize(img, (400, 400))
    # 读入的图像数据格式是[H, W, C]
    # 使用转置操作将其变成[C, H, W]
    img = np.transpose(img, (2, 0, 1)).astype('float32')
    # 将数据范围调整到[0.0, 1.0]之间
    if flag == 1:
        img = img / 255.
    return img

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

