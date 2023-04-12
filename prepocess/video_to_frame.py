import cv2
import numpy as np
import os
import numpy as np
import math
import argparse

def video2frame(input_video_path, ouput_image_path):
    """
    video convert to image
    video type is .MP4
    """

    video_root_file = []

    for i in os.listdir(input_video_path):
        full_path = os.path.join(input_video_path, i)
        if full_path.endswith('.MP4'):  # Modifiable suffix
            video_root_file.append(full_path)
    
    if os.path.isdir(ouput_image_path):
        print('output path already exists!')
    else:
        os.makedirs(ouput_image_path) 
    
    video_num = len(video_root_file)
    
    if video_num != 0:
        State = True
    else:
        print('The video path is incorrect, or the number of videos is 0.')
    
    for i in range(video_num):
        # Each video is traversed for frame extraction and saving
        cap = cv2.VideoCapture(video_root_file[i])
        fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # float
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
        print("fps:",fps)
        print("h,w:",height, width)
        cap.set(cv2.CAP_PROP_FPS, 0)  

        video_name = video_root_file[i].split('/')[-1][:-4]
        video_name_file = os.path.join(ouput_image_path, video_name)

        if os.path.isdir(video_name_file):
            pass
        else:
            os.makedirs(video_name_file)
        
        imageNum = 0
        while State:
            capState, frame = cap.read()
            imageNum += 1
            if capState == True and (imageNum % fps) == 0:
                # save image
                cv2.imwrite(video_name_file + "/" + video_name.split('\\')[1] + str(int(imageNum / fps)) + '.jpg', frame)
            if capState == False:
                cap.release()
                break
            
        print('-----------',video_name,'-----------')
    
    print("----------------video to frame end---------------------------")


def main():
    parser = argparse.ArgumentParser(description="Convert video to frame, 1 frame in 1 second.")
    parser.add_argument("--input_video_path", default="D:/SomeCodes/SensLoc/datasets/jinxia/query/video/seq4")
    parser.add_argument("--output_image_path", default="D:/SomeCodes/SensLoc/datasets/jinxia/query/image/")
    args = parser.parse_args()

    video2frame(input_video_path=args.input_video_path, ouput_image_path=args.output_image_path)

if __name__ == "__main__":
    main()
