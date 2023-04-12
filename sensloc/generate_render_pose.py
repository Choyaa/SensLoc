import numpy as np
import os
import glob
import pandas as pd
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import argparse


def parse_image_list(path):
    images = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if len(line) == 0 or line[0] == '#':
                continue
            name, *data = line.split()
            model, width, height, *params = data
            params = np.array(params, float)
            images[os.path.basename(name).split('.')[0]] = (model, int(width), int(height), params)
  
    assert len(images) > 0
    return images

def qvec2rotmat(qvec):  #!wxyz
    return np.array([
        [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
         2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
         2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
        [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
         1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
         2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
        [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
         2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
         1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

def rotmat2qvec(R):
    Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz, Rzz = R.flat
    K = np.array([
        [Rxx - Ryy - Rzz, 0, 0, 0],
        [Ryx + Rxy, Ryy - Rxx - Rzz, 0, 0],
        [Rzx + Rxz, Rzy + Ryz, Rzz - Rxx - Ryy, 0],
        [Ryz - Rzy, Rzx - Rxz, Rxy - Ryx, Rxx + Ryy + Rzz]]) / 3.0
    eigvals, eigvecs = np.linalg.eigh(K)
    qvec = eigvecs[[3, 0, 1, 2], np.argmax(eigvals)]
    if qvec[0] < 0:
        qvec *= -1
    return qvec

def parse_pose_list(path, origin_coord):
    poses = {}
    X = []
    Y = []
    Z = [] # 存放x，y的位置
    q_list = []
    with open(path, 'r') as f:
        for data in f.read().rstrip().split('\n'):
            data = data.split()
            name = (data[0].split('/')[-1]).split('.')[0]
            q, t = np.split(np.array(data[1:], float), [4])
            
            R = np.asmatrix(qvec2rotmat(q)).transpose()  #c2w
            
            T = np.identity(4)
            T[0:3,0:3] = R
            T[0:3,3] = -R.dot(t)   #!  c2w

            if origin_coord is not None:
                origin_coord = np.array(origin_coord)
                T[0:3,3] -= origin_coord
            transf = np.array([
                [1,0,0,0],
                [0,-1,0,0],
                [0,0,-1,0],
                [0,0,0,1.],
            ])
            T = T @ transf

            X.append(T[0,3])
            Y.append(T[1,3])
            Z.append(T[2,3])
            q_list.append([q])
            
            
            poses[name] = T
            
    
    assert len(poses) > 0
    return poses, X, Y, Z, q_list

def euler2quad(euler):
    """
    欧拉转四元数（xyzw）
    """
    ret = R.from_euler('xyz', euler,degrees=True)
    quad = ret.as_quat()

    return quad

def write_pose(db_pose_file, db_intrinsic_file, euler_path, write_path, intrinsic, origin_coord=[399961, 3138435, 0]):
    """
    db_pose_file: wumu_pose
    db_intrinsic_file: wumu_intrinsic
    euler_path: blender render angle (.txt)
    write_path: render path
    intrinsic: [w,h,fx,fy]
    origin_coord:
    """
    poses, X, Y, Z, _ = parse_pose_list(db_pose_file, origin_coord)
    wumu_intrinsic = parse_image_list(db_intrinsic_file)

    write_pose_path = write_path + '/' + 'pose.txt'
    write_intrinsic_path = write_path + '/' + 'intrinsic.txt'

    all_euler = []
    quad_name = ['z', 'y', 'x', 'q', 'h', 'zq', 'yq', 'zh', 'yh', 'xz', 'xzz', 'xzzz', 'xzzzz', 'xy', 'xyy', 'xyyy']
    all_quad = []

    names = list(wumu_intrinsic.keys())

    with open(euler_path, 'r') as f_r:
        for line in f_r:
            line = line.strip('\n')
            euler = line.split(' ')
            all_euler.append([-180+eval(euler[1]),eval(euler[2]), eval(euler[3])])
            temp_quad = euler2quad(all_euler[-1])
            ret = R.from_quat(temp_quad)
            matrix = ret.as_matrix()
            temp_quad = rotmat2qvec(matrix.T)
            all_quad.append(temp_quad)

    with open(write_pose_path, 'w') as file_pose:
        for name in names:
            for i in range(len(all_euler)):
                R1 = np.asmatrix(qvec2rotmat(all_quad[i]))
                T = np.identity(4)
                T[0:3, 0:3] = R1
                T[0:3, 3] = -R1.dot(np.array([X[i]+origin_coord[0], Y[i]+origin_coord[1], 200+origin_coord[2]]))
                out_line =  str(name) + quad_name[i] + '.JPG' + ' ' + str(all_quad[i][0]) + ' ' + str(all_quad[i][1]) + ' ' + str(all_quad[i][2]) + ' ' + str(all_quad[i][3]) + ' ' + str(T[0:3, 3][0]) + ' ' + str(T[0:3, 3][1]) + ' ' + str(T[0:3, 3][2]) + '\n'
                file_pose.write(out_line)

    w,h,fx,fy = intrinsic
    with open(write_intrinsic_path, 'w') as file_intri:
        for name in names:
            for i in range(len(all_euler)):
                out_line = 'db/' + str(name) + '.JPG' + ' ' + 'PINHOLE' + ' ' + str(w) + ' ' + str(h) + ' ' + str(fx) + ' ' + str(fy) + ' ' + str(w//2) + ' ' + str(h//2) + '\n'
                file_intri.write(out_line)

def main():

    parser = argparse.ArgumentParser(description="Generate render db pose file and intrinsic file.")
    parser.add_argument("--db_wu_pose", default="D:/SomeCodes/SensLoc/datasets/jinxia/db/wumu_pose/db_pose.txt")
    parser.add_argument("--db_wu_intrinsic", default="D:/SomeCodes/SensLoc/datasets/jinxia/db/wumu_pose/db_intinsics.txt")
    parser.add_argument("--euler_txt", default="D:/SomeCodes/SensLoc/datasets/jinxia/db/render_pose/bamu_euler.txt")
    parser.add_argument("--write_render_path", default="D:/SomeCodes/SensLoc/datasets/jinxia/db/render_pose/")
    parser.add_argument('--intrinsic', default=[1920,1080,1400.3421449,1065.78947])
    args = parser.parse_args()

    write_pose(args.db_wu_pose, args.db_wu_intrinsic, args.euler_txt, args.write_render_path, args.intrinsic)




if __name__ == "__main__":
    
    main()
   

    





