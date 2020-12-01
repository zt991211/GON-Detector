from models import DeepModel
import cv2
from PIL import Image
import numpy as np
from skimage.measure import label,regionprops
from tools import BW_img,disc_crop

#some hyper parameters
Disc_ROI=600
Unet_size=640

#init my unet model
unet_weights_url='model_weights/Model_DiscSeg_ORIGA.h5'
my_unet_model=DeepModel(Unet_size)
my_unet_model.load_weights(unet_weights_url)

#return a ROI PIL Image
def getROI(path):
    old_img = Image.open(path)
    org_img = np.array(old_img)
    # main algorithm
    test_img = old_img.resize((Unet_size, Unet_size))
    test_img = np.array(test_img)
    test_img = np.reshape(test_img, (1,) + test_img.shape)
    disc_map = my_unet_model.predict([test_img])
    disc_map = BW_img(np.reshape(disc_map, (Unet_size, Unet_size)), 0.5)
    regions = regionprops(label(disc_map))

    # orginal coordinate
    C_x = int(regions[0].centroid[0] * org_img.shape[0] / 640)
    C_y = int(regions[0].centroid[1] * org_img.shape[1] / 640)

    # crop img and label and PT,both ndarray are (600,600,3)
    disc_region, err_coord, crop_coord = disc_crop(org_img, Disc_ROI, C_x, C_y)

    # clahe algorithm
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    R, G, B = cv2.split(disc_region)
    new_R = clahe.apply(R)
    new_G = clahe.apply(G)
    new_B = clahe.apply(B)
    disc_region = cv2.merge((new_R, new_G, new_B))

    # transform the dataset
    disc_Image = Image.fromarray(disc_region.astype(np.uint8))
    return disc_Image

test_path='test_img/V0001.jpg'
target=getROI(test_path)
target.show()
#target.save('E:\\results\\2.png')