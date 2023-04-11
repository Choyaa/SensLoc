import cv2
import os
import numpy as np
import torch
import h5py
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"
exr_file = "/home/ubuntu/Documents/dataset/jinxia/wide_angle_0/depth/17y007990005.exr"
# save_path = '/home/ubuntu/Documents/1-pixel/render/geo/results/'
image = cv2.imread(exr_file, cv2.IMREAD_UNCHANGED)


print(image.shape, np.max(image), np.min(image))


depth=cv2.split(image)[0]
depth[depth>1000]=0
depth=depth/500.00

scale = 4
# imgq_resize = cv2.resize(depth, (int(depth.shape[1]/scale), int(depth.shape[0]/scale)))
cv2.imshow('imgOri',depth) 
cv2.waitKey(0)   



