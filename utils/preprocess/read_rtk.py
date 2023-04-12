from tkinter import SW
import exifread
import os
import glob
import numpy as np
import pandas as pd
import cv2
import time
import math

def read_file(img_file):
    """
    :param img_file:
    :return:
    """

    img_list = []
    img_list += glob.glob(os.path.join(img_file, "*.{}").format('jpg'))

    if len(img_list) != 0:
        return img_list
    else:
        print("img_file is wrong, there is no image")

def Read_RTK_of_query(csv_save_path):
    
    
    ground_truth_information = pd.read_csv('./1126-2_点层.csv', encoding = 'gb2312')   #!rtk image
    roll = csv_information['roll']
    pitch = csv_information['pitch']
    yaw = csv_information['yaw']


    img_name_list = []
    point_list = []
    qz_list = []
    qy_list = []
    qx_list = []
    qw_list = []
    gps_lon_list = []
    gps_lat_list = []
    gps_alt_list = []

    roll_list = []
    pitch_list = []
    yaw_list = []

    match_bool = False

    num_j = 0
    num_k = 0

    fd_out = open(iphone_prior_output, 'w')
    path_list = os.listdir(img_list)
    path_list.sort(key=lambda x:int(x[4:-4]))
    for img in path_list:
        img_information = exifread.process_file(open(os.path.join(img_list, img), 'rb'))
        # import ipdb;ipdb.set_trace();
        time_img = img_information['Image DateTime'].values
        new_time = time_img[11:17] # 手机时间 #time_img[:4] + '-' + time_img[5:7] + '-' + 
        second = time_img[17:]
        new_time = new_time + str(int(second))
        
        # # GPS转换
        count = 1
        info_name = csv_information["loggingSample(N)"]
        to_write = []
        start_time = 57684
        for j in range(len(info_name)):
            if float(csv_information['locationAltitude(m)'][j]) == 0:
                continue
            else:
                # timeArray = time.localtime(csv_information['locationTimestamp_since1970(s)'][j])
                # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                Hours = int(csv_information['loggingTime(txt)'][j][11:13])
                Minutes = int(csv_information['loggingTime(txt)'][j][14:16])
                Seconds = int(csv_information['loggingTime(txt)'][j][17:19])
                # print(new_time, prior_time)
                prior_time = csv_information['loggingTime(txt)'][j][11:13]+':'+csv_information['loggingTime(txt)'][j][14:16]+':'+ str(int(csv_information['loggingTime(txt)'][j][17:19])+2)

                if new_time == prior_time:
                    print(new_time)
                    info_TIME = Hours*3600 + Minutes*60 + Seconds
                    Index = info_TIME - start_time + 1
                    # print(img)
                    fd_out.write(img)
                    # fd_out.write(info_name[j] + ' ')

                    gps_lon = csv_information['locationLongitude(WGS84)'][j]
                    gps_lat = csv_information['locationLatitude(WGS84)'][j]
                    gps_alt = float(csv_information['locationAltitude(m)'][j])-12
                    to_write.extend([str(gps_lon), str(gps_lat) ,str(gps_alt)])
                    # yaw, pitch, roll = csv_information['yaw'][j], csv_information['pitch'][j], csv_information['roll'][j]
                    x, y, z, w = csv_information['motionQuaternionX(R)'][j], csv_information['motionQuaternionY(R)'][j], 
                    csv_information['motionQuaternionZ(R)'][j], csv_information['motionQuaternionW(R)'][j], 

                    to_write.extend([yaw, pitch ,roll])

                    line_ = " ".join([str(elem) for elem in to_write])
                    fd_out.write(line_ + "\n")
                    count += 1
            to_write=[]
    print("Done with writting iphone.txt")
    fd_out.close() 
img_list = read_file('/home/ubuntu/Documents/1-pixel/1-jinxia/拍摄1126/phone/day1')   #!image
img_list = '/home/ubuntu/Documents/1-pixel/1-jinxia/拍摄1126/phone/day1'

time_list = []

csv_information = pd.read_csv('./prior1.csv', encoding = 'gb2312')

csv_save_path = "./construct11_26.csv"  #!save_path
iphone_prior_output = "./day1_prior.txt"
  
        