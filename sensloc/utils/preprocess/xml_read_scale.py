from tokenize import Name
import xmltodict
import json
import numpy as np
from scipy.spatial.transform import Rotation
from decimal import Decimal
import time
import os

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

def rotation_to_quat (rotation_metrix):
    a = []
    for k,v1 in rotation_metrix.items():
        if k in 'Accurate':
            continue
        a.append(float(v1))
    a_np = np.array(a)
    a_np = a_np.reshape(3, 3)
    a_qvec = rotmat2qvec(a_np)# w,x,y,z
    return a_qvec, a_np

def TxTyTz_trans(metirx, r):
    a = []
    for k,v1 in metirx.items():
        if k in 'Accurate':
            continue
        a.append(float(v1))
    a_np = np.array(a)
    a_np = a_np.reshape(3, 1)
    a_np1 = -r @ a_np
    tx, ty, tz= a_np1.flat
    return tx, ty, tz, a_np1

def transfer_rxyz(R, t):
    # invert
    t = -R.T @ t
    R = R.T

    R[:, 2] *= -1
    R[:, 1] *= -1

    #invert back
    t = -R.T @ t
    R = R.T

    tx, ty, tz = t.flat
    return R, tx, ty, tz

def write_cameras_text_oneGroup(dictdata, camera_path, Camera_models, num_group):
    HEADER_cemera = "# Camera list with one line of data per camera:\n" + \
             "#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n" + \
             "# Number of cameras: {}\n".format(num_group)
    with open (camera_path, "w") as fd:
        fd.write(HEADER_cemera)
        cam_id = 0
        cam_model = Camera_models
        # import ipdb;ipdb.set_trace();
        cam_width = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['ImageDimensions']['Width']
        cam_height = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['ImageDimensions']['Height']
        cam_FocalLenth = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['FocalLengthPixels']
        cam_px = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['PrincipalPoint']['x']
        cam_py = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['PrincipalPoint']['y']
        cam_k1 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['Distortion']['K1']
        cam_k2 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['Distortion']['K2']
        cam_k3 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['Distortion']['K3']
        cam_p1 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['Distortion']['P1']
        cam_p2 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup']['Distortion']['P2']
        if cam_model == 'PINHOLE':
            to_write = [cam_id, cam_model,cam_width,cam_height,cam_FocalLenth,cam_FocalLenth, cam_px,cam_py]
        elif cam_model == 'FULL_OPENCV':
            to_write = [cam_id, cam_model,cam_width,cam_height,cam_FocalLenth,cam_FocalLenth, cam_px,cam_py, cam_k1, cam_k2, cam_p1, cam_p2, cam_k3, 0, 0, 0]
        line = " ".join([str(elem) for elem in to_write])
        fd.write(line + "\n")
    print("Camera write. Done!")
    return 0

def write_images_text_oneGroup(dictdata, image_path, num_group, sample_sacle, prefix_word, tilepoints_dict, num_pergroup):
    HEADER_image = "# Image list with two lines of data per image:\n" + \
             "#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n" + \
             "#   POINTS2D[] as (X, Y, POINT3D_ID)\n" + \
             "# Number of images: {}, mean observations per image: {}\n".format(len(tilepoints_dict), 'xxx')
    
    fd = open(image_path, 'w')
    fd.write(HEADER_image)
    count = 0
    count_tile = 0
    for i in range(num_group):
        Photogroup_item = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]
        count, count_tile = iamge_txt_for(Photogroup_item, fd, count, count_tile, i, sample_sacle, prefix_word, tilepoints_dict, num_pergroup)
    
    print("Write {} images. Done!".format(count))
    fd.close()
    return 0

def write_cameras_text(dictdata, camera_path, Camera_models, num_group):
    HEADER_cemera = "# Camera list with one line of data per camera:\n" + \
             "#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n" + \
             "# Number of cameras: {}\n".format(num_group)
    with open (camera_path, "w") as fd:
        fd.write(HEADER_cemera)
        for i in range(num_group):
            cam_id = i
            cam_model = Camera_models
            import ipdb;ipdb.set_trace();
            cam_width = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['ImageDimensions']['Width']
            cam_height = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['ImageDimensions']['Height']
            cam_FocalLenth = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['FocalLengthPixels']
            cam_px = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['PrincipalPoint']['x']
            cam_py = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['PrincipalPoint']['y']
            cam_k1 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['Distortion']['K1']
            cam_k2 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['Distortion']['K2']
            cam_k3 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['Distortion']['K3']
            cam_p1 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['Distortion']['P1']
            cam_p2 = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]['Distortion']['P2']
            if cam_model == 'PINHOLE':
                to_write = [cam_id, cam_model,cam_width,cam_height,cam_FocalLenth,cam_FocalLenth, cam_px,cam_py]
            elif cam_model == 'FULL_OPENCV':
                to_write = [cam_id, cam_model,cam_width,cam_height,cam_FocalLenth,cam_FocalLenth, cam_px,cam_py, cam_k1, cam_k2, cam_p1, cam_p2, cam_k3, 0, 0, 0]
            line = " ".join([str(elem) for elem in to_write])
            fd.write(line + "\n")
    print("Camera write. Done!")
    return 0

def iamge_txt_for(Photogroup_item,fd, count,count_tile, i, sample_sacle,prefix_word, tilepoints_dict, num_pergroup):
    Cam_Id = i
    for k,v in Photogroup_item.items():
        if k == 'Photo':
            for j in range((len(Photogroup_item[k]))):
                    # Image_Id
                Image_Id = Photogroup_item[k][j]['Id']
                    # Image_Name
                Name = prefix_word + Photogroup_item[k][j]['ImagePath'].split('\\')[-1]
                    # quat Qw,Qx,Qy,Qz  Caution: R：W2C， T：C2W
                rotation_metrix = Photogroup_item[k][j]['Pose']['Rotation']
                qvec, r = rotation_to_quat(rotation_metrix)
                    # Tx,Ty,Tz   Caution: R：W2C， T：C2W
                TxTyTz_metirx = Photogroup_item[k][j]['Pose']['Center']
                tx, ty, tz, t = TxTyTz_trans(TxTyTz_metirx, r)
                    # invert
                r, tx ,ty, tz = transfer_rxyz(r, t)
                qvec = rotmat2qvec(r)

                if  tilepoints_dict[count_tile]['PhotoId'] != Image_Id:
                    to_write = [Image_Id, qvec[0],qvec[1],qvec[2],qvec[3],tx,ty,tz,Cam_Id, Name]
                    line = " ".join([str(elem) for elem in to_write])
                    line2 = ""
                    count += 1
                    print("There has no points corespond to {}th image_id".format(Image_Id))
                    
                else: 
                    to_write = [Image_Id, qvec[0],qvec[1],qvec[2],qvec[3],tx,ty,tz,Cam_Id, Name]
                    to_write_tilepoints= tilepoints_dict[count_tile]['position']
                    line = " ".join([str(elem) for elem in to_write])
                    line2 = " ".join([str(elem) for elem in to_write_tilepoints])
                    count += 1
                    count_tile += 1
                


                if (int(Photogroup_item[k][j]['Id'])- num_pergroup*i) % sample_sacle ==0:
                    fd.write(line + "\n")
                    fd.write(line2 + "\n")

    return count, count_tile


def write_images_text(dictdata, image_path, num_group, sample_sacle, prefix_word, tilepoints_dict, num_pergroup):
    HEADER_image = "# Image list with two lines of data per image:\n" + \
             "#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n" + \
             "#   POINTS2D[] as (X, Y, POINT3D_ID)\n" + \
             "# Number of images: {}, mean observations per image: {}\n".format(len(tilepoints_dict), 'xxx')
    
    fd = open(image_path, 'w')
    fd.write(HEADER_image)
    count = 0
    count_tile = 0
    for i in range(num_group):
        Photogroup_item = dictdata['BlocksExchange']['Block']['Photogroups']['Photogroup'][i]
        count, count_tile = iamge_txt_for(Photogroup_item, fd, count, count_tile, i, sample_sacle, prefix_word, tilepoints_dict, num_pergroup)
    
    print("Write {} images. Done!".format(count))
    fd.close()
    return 0

def extract_points3D (dictdata,simplepoints_path):
    HEADER_points = "# Simple 3D point list with one line of data per point:\n" + \
             "#   POINT3D_ID, X, Y, Z, R, G, B\n"
    
    fd = open(simplepoints_path, 'w')
    fd.write(HEADER_points)
    
    count = 0
    tilponts = dictdata['BlocksExchange']['Block']['TiePoints']['TiePoint']

    for i in range(len(tilponts)):
        points_id = i
        if 'Position' in tilponts[i].keys():
            X, Y ,Z = tilponts[i]['Position']['x'], tilponts[i]['Position']['y'], tilponts[i]['Position']['z']
            R, G ,B = tilponts[i]['Color']['Red'], tilponts[i]['Color']['Green'], tilponts[i]['Color']['Blue']
            to_write = [points_id, X, Y, Z, int(float(R)*255.0), int(float(G)*255.0), int(float(B)*255.0)]
            line = " ".join([str(elem) for elem in to_write])
            fd.write(line + "\n")
            count += 1
    
    print("Extract {} points3D. Done!".format(count))
    fd.close()
    return 0


def write_points(dictdata, points_path, tile3Dpoints_dict):
    HEADER_points = "# 3D point list with one line of data per point:\n" + \
             "#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)\n" + \
             "# Number of points: {}, mean track length: {}\n".format(len(tile3Dpoints_dict), 0)
    
    fd = open(points_path, 'w')
    fd.write(HEADER_points)

    count = 0
    tilponts = dictdata['BlocksExchange']['Block']['TiePoints']['TiePoint']

    assert len(tilponts) == len(tile3Dpoints_dict)


    for i in range(len(tilponts)):
        assert int(tile3Dpoints_dict[i]['3D_Id']) == (i)
        points_id = i
        # import ipdb; ipdb.set_trace();
        if 'Position' in tilponts[i].keys():
            X, Y ,Z = tilponts[i]['Position']['x'], tilponts[i]['Position']['y'], tilponts[i]['Position']['z']
            R, G ,B = tilponts[i]['Color']['Red'], tilponts[i]['Color']['Green'], tilponts[i]['Color']['Blue']
            error_projection = '0'
            to_write = [points_id, X, Y, Z, int(float(R)*255.0), int(float(G)*255.0), int(float(B)*255.0), error_projection]
            to_write.extend(tile3Dpoints_dict[i]['position'])
            line = " ".join([str(elem) for elem in to_write])
            fd.write(line + "\n")
            count += 1
    
    print("Extract {} points3D. Done!".format(count))

    fd.close()
    return 0


def extract_2Dtilepoints(dictdata, num_group):
    tilponts = dictdata['BlocksExchange']['Block']['TiePoints']['TiePoint']
    
    a = []
    for i in range(len(tilponts)):
        d_up = {'3D_Id': '{}'.format(i)}
        for j in tilponts[i]['Measurement']:
            j.update(d_up)
        a.extend(tilponts[i]['Measurement'])
    
    # sort
    a_new_list = sorted(a, key=lambda k: int(k['PhotoId']))
    num_pergroup = int((int(a_new_list[-1]['PhotoId'])+1)/num_group)
    # category
    m = {}
    for i in a_new_list:
        rid = str(i['PhotoId'])
        m.setdefault(rid, {
          'PhotoId': rid,
          'position':[]
        })['position'].extend(list((i['x'], i['y'], i['3D_Id'])))

    return list(m.values()), a_new_list, num_pergroup

def extract_3Dtilepoints(dictdata):

    # tag the 2D_indx
    pthoto_indx = 0 # initialize
    points2D_indx = 0
    for item in dictdata:
        if pthoto_indx == int(item['PhotoId']):
            item.update({'2D_indx':points2D_indx})
            points2D_indx += 1
        else:
            pthoto_indx = int(item['PhotoId'])
            points2D_indx = 0
            item.update({'2D_indx':points2D_indx})
            points2D_indx += 1

    # sort by 3D_id
    a_new_list = sorted(dictdata, key=lambda k: int(k['3D_Id']))
    # category
    m = {}
    for i in a_new_list:
        rid = str(i['3D_Id'])
        m.setdefault(rid, {
          '3D_Id': rid,
          'position':[]
        })['position'].extend(list((i['PhotoId'], str(i['2D_indx']))))
    # print(list(m.values()))
    return list(m.values())

def main(config):
    
    xml_dir = config['xml_dir']
    num_group = config['num_group']  #number of camera
    Camera_models = config['Camera_models'] # cameral model, PINHOLE or FULL_OPENCV
    camera_path = config['camera_path']
    image_path = config['image_path']
    points_path = config['points_path']
    simplepoints_path = config['simplepoints_path'] # Just for (X, Y, Z, R, G ,B)
    sample_sacle = config['sample_sacle']
    prefix_word = config['prefix_word']
    flag = config['flag']

    if flag == 0:
        print("There is no need for .xml reading")
        return 0

    if not os.path.exists('./colmap'):
        os.mkdir('./colmap')

    # ============ Read .xml files =============
    print("Reading {}...".format(xml_dir.split('/')[-1]))

    file_object = open(xml_dir, encoding = 'utf-8')
    try:
        all_the_xmlStr = file_object.read()
    finally:
        file_object.close()
    # transfer to dict
    dictdata = dict(xmltodict.parse(all_the_xmlStr))
    # extract tilepoints for following step
    tile2Dpoints_dict, tilepoints_measurement, num_pergroup = extract_2Dtilepoints(dictdata, num_group)

    # ============ Transfer to .json==============
    # jsonStr = json.dumps(dictdata,ensure_ascii=False)
    # with open('./XResults.json', 'w',encoding = 'utf-8') as f:
    #     f.write(jsonStr.replace('@', ''))

    # ============= Write camera.txt =================
    print("===== " + "Writing camera.txt to {}".format(camera_path) + " =====")
    write_cameras_text(dictdata, camera_path, Camera_models, num_group)
            
    # ============ Write image.txt =====================
    print("===== " +"Writing image.txt to {}, sample scale: {}".format(image_path, sample_sacle)+ " =====")

    write_images_text(dictdata, image_path, num_group, sample_sacle, prefix_word, tile2Dpoints_dict, num_pergroup)

    # ============ Write points3D.txt ===================
    print("===== " + "Writing points3D.txt to {}".format(points_path) + " =====")

    tile3Dpoints_dict = extract_3Dtilepoints(tilepoints_measurement)
    write_points(dictdata, points_path, tile3Dpoints_dict)

    # ============ Extract 3D Points=====================
    extract_points3D(dictdata, simplepoints_path)

if __name__ == "__main__":
    path  = "/home/ubuntu/Documents/dataset/jinxia/2_colmap/"
    xml_dir = path+"XResult-A3-rotation.xml"
    num_group = 5  #number of camera
    Camera_models = 'FULL_OPENCV' # cameral model, PINHOLE or FULL_OPENCV
    camera_path = path+'cameras.txt'
    image_path = path+'images.txt'
    points_path = path+'points3D.txt'
    simplepoints_path = path+'simplepoints3D.txt' # Just for (X, Y, Z, R, G ,B)
    sample_sacle = 1
    prefix_word = 'db/'
    flag = 1

    config_manual = {
        "xml_dir" : xml_dir,
        "num_group" : num_group,  
        "Camera_models" : Camera_models, 
        "camera_path" : camera_path,
        "image_path" : image_path,
        "points_path" : points_path,
        "simplepoints_path" : simplepoints_path, 
        "sample_sacle" : sample_sacle,
        "prefix_word" : prefix_word,
        "flag" : flag
    }

    main(config_manual)