import numpy as np
import os
import glob
import pandas as pd
from pyproj import Transformer
from pyproj import CRS
from scipy.spatial.transform import Rotation as R
import argparse
from utils.transfrom import qvec2rotmat,rotmat2qvec, compute_pixel_focal


def read_SRT_to_txt(input_SRT_file, output_txt_file, intrinsic, fps, GROUPLENGTH):
    """
    input_SRT_file: SRT path file
    out_txt_file: txt path file
    intrinsic:[w, h, sensorW, sensorH, cx, cy, focal]
    GROUPLENGTH: How many rows are in a group
    """

    width, height, sensorW, sensorH, cx, cy, focal_len = intrinsic[:]

    SRT_root_file = []
    for i in os.listdir(input_SRT_file):
        full_path = os.path.join(input_SRT_file, i)
        if full_path.endswith('.SRT'): 
            SRT_root_file.append(full_path)
    
    if os.path.isdir(output_txt_file):
        pass
    else:
        os.makedirs(output_txt_file)

    SRT_num = len(SRT_root_file)
    
    if SRT_num != 0:
        State = True
    else:
        print('The srt path is incorrect, or the number of file is 0.')
    
    for i in range(SRT_num):
        with open(SRT_root_file[i]) as f:
            information = f.readlines()
        
        SRT_name = SRT_root_file[i].split('/')[-1][:-4]
        SRT_name_file = output_txt_file + '/'  + SRT_name + '_' + 'pose.txt'
        SRT_name_file_intrinsic = output_txt_file + '/'  + SRT_name + '_' + 'intrinsic.txt'

        with open(SRT_name_file,'w') as file_w:
            for i in range(len(information)//GROUPLENGTH):
                if i % fps == 0:
                    frameCount = eval(information[i * GROUPLENGTH])
                    position = information[(frameCount-1)*GROUPLENGTH+5].split(':')
                    lat, lon, alt = eval(position[1].split(']')[0]),eval(position[2].split(']')[0]), eval(position[3].split(' ')[1])
                    oritation = information[(frameCount-1)*GROUPLENGTH+8].split(' ')
                    yaw, pitch, roll = eval(oritation[1]),eval(oritation[3]),eval(oritation[5][:-1])

                    # GPS转世界坐标
                    crs_CGCS2000 = CRS.from_wkt('PROJCS["CGCS_2000_3_Degree_GK_CM_114E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",114.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]')  # degree
                    crs_WGS84 = CRS.from_epsg(4326)
                    from_crs = crs_WGS84
                    to_cgcs = crs_CGCS2000
                    transformer = Transformer.from_crs(from_crs, to_cgcs)
                    new_x, new_y = transformer.transform(lat, lon)

                    # 欧拉角转四元数
                    euler = [yaw,pitch,roll]
                    ret = R.from_euler('zxy',[float(euler[0]), 90-float(euler[1]), float(euler[2])],degrees=True)
                    R_matrix = ret.as_matrix()
                    qw, qx, qy, qz = rotmat2qvec(R_matrix)

                    # c2w
                    q = [qw, qx, qy, qz]
                    R1 = np.asmatrix(qvec2rotmat(q))
                    T = np.identity(4)
                    T[0:3, 0:3] = R1
                    T[0:3, 3] = -R1.dot(np.array([new_x, new_y, alt]))

                    out_line_str = SRT_name + str(int((i+1) / fps)) + ' ' + str(qw) + ' ' + str(qx) + ' ' + str(qy) + ' ' + str(qz) + ' ' + str(T[0:3, 3][0]) + ' ' + str(T[0:3, 3][1]) + ' ' + str(T[0:3, 3][2]) + '\n'
                    file_w.write(out_line_str)   
                    # print(i)
        print("------------", SRT_name, "pose end------------")
        

        with open(SRT_name_file_intrinsic, 'w') as file_in_w:
            for i in range(len(information)//GROUPLENGTH):
                if i % fps == 0:
                # focal_len_list = information[i*GROUPLENGTH+4].split(':') # eq_len
                # focal_len = eval(focal_len_list[5].split(' ')[1][:-1])
                    fx, fy = compute_pixel_focal(sensorH, sensorW, focal_len, width, height)
                    out_line_str = SRT_name + str(int((i+1) / fps)) + ' ' + 'PINHOLE' + ' ' + str(width) + ' ' + str(height) + ' ' + str(fx) + ' ' + str(fy) + ' ' + str(cx) + ' ' + str(cy) + '\n'
                    file_in_w.write(out_line_str)

        print("------------", SRT_name, "intrinsic end------------")

def main():
    
    parser = argparse.ArgumentParser(description="write SRT information (name qw qx qy qz x y z) in txt file")
    parser.add_argument("--input_SRT_path", default="D:/SomeCodes/SensLoc/datasets/jinxia/query/video/SRT/W/")
    parser.add_argument("--output_txt_path", default="D:/SomeCodes/SensLoc/datasets/jinxia/query/txt/SRT/W/")
    parser.add_argument("--sensorW", default=6.16)
    parser.add_argument("--sensorH", default=4.62)
    parser.add_argument("--imgWidth", default=1920)
    parser.add_argument("--imgHeight", default=1080)
    parser.add_argument("--focal_length", default=4.5)
    parser.add_argument("--GROUPLENGTH", default=14)
    parser.add_argument("--fps", default=30)
    args = parser.parse_args()
    intrinsic = [args.imgWidth, args.imgHeight, args.sensorW, args.sensorH, args.imgWidth//2, args.imgHeight//2, args.focal_length]

    read_SRT_to_txt(args.input_SRT_path, args.output_txt_path, intrinsic, args.fps, args.GROUPLENGTH)


if __name__ == "__main__":

    main()