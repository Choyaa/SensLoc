dji_day2

/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/djiday2/reference_rgb.blend \
-P /home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization/lib/dji_rgb.py \
-- /home/ubuntu/Documents/1-pixel/1-jinxia/jinxia_datasets/queries_intrinsics/que/dj_day2_intrinsics.txt  \
/home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization/AirLoc/queries_gt/single/dj_day2_gt.txt \
/home/ubuntu/Documents/blender_render/nerf1/   

/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/djiday2/reference.blend \
-P /home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization/lib/dji_depth.py  \
-- /home/ubuntu/Documents/1-pixel/1-jinxia/jinxia_datasets/queries_intrinsics/que/dj_day2_intrinsics.txt  \
/home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization/AirLoc/queries_gt/single/dj_day2_gt.txt \
/home/ubuntu/Documents/blender_render/nerf1/ 


phone
 /home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
 -b /home/ubuntu/Documents/1-pixel/blender_demo/reference_rgb.blend \
 -P /home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization/lib/phone_rgb.py \
 --  /home/ubuntu/Documents/1-pixel/1-jinxia/jinxia_datasets/queries_intrinsics/que/phone_day2_intrinsics.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/jinxia_datasets/queries_gt/single/phone_day2_gt.txt   \
/home/ubuntu/Documents/blender_render/nerf/   

 /home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
 -b /home/ubuntu/Documents/1-pixel/blender_demo/reference.blend \
 -P /home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization/lib/phone_depth.py \
 --  /home/ubuntu/Documents/1-pixel/1-jinxia/jinxia_datasets/queries_intrinsics/que/phone_day2_intrinsics.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/jinxia_datasets/queries_gt/single/phone_day2_gt.txt   \
/home/ubuntu/Documents/blender_render/nerf/  

reference
/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/reference/reference_rgb.blend \
-P /home/ubuntu/Documents/code/视频抽帧/src/blender_rendering/db_rgb.py \
-- /home/ubuntu/Documents/code/SensorLoc/datasets/wide_angle/sup/new_intrinsic.txt \
/home/ubuntu/Documents/code/SensorLoc/datasets/wide_angle/sup/new_pose.txt \
/home/ubuntu/Documents/code/SensorLoc/datasets/wide_angle/sup/db_200_2/

/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/reference/reference_rgb.blend \
-P /home/ubuntu/Documents/code/视频抽帧/src/blender_rendering/db_rgb.py \
-- /home/ubuntu/Documents/1-pixel/1-jinxia/Hierarchical-Localization/datasets/wide_angle/sup/db_intinsics.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/Hierarchical-Localization/datasets/wide_angle/sup/db_pose_200.txt \
/home/ubuntu/Documents/dataset/jinxia/wide_angle/sup/db_focal/
gt
/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/reference/reference_rgb.blend \
-P /home/ubuntu/Documents/code/视频抽帧/src/blender_rendering/db_rgb.py \
-- /home/ubuntu/Documents/code/SensorLoc/datasets/wide_angle/queries/30_intrinsics.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/Hierarchical-Localization/datasets/wide_angle/sensors/gt_pose.txt \
/home/ubuntu/Documents/dataset/jinxia/wide_angle/sup/db_focal/
es
/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/reference/reference_rgb.blend \
-P /home/ubuntu/Documents/code/视频抽帧/src/blender_rendering/db_rgb.py \
-- /home/ubuntu/Documents/1-pixel/1-jinxia/Hierarchical-Localization/datasets/zoom/new_intrinsic_line_test.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/Hierarchical-Localization/datasets/zoom/new_pose_line_test.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/Hierarchical-Localization/datasets/zoom/render_db/


/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/reference/reference_rgb.blend \
-P /home/ubuntu/Documents/code/视频抽帧/src/blender_rendering/db_rgb.py \
-- /home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization_github_complete/results/wide_angle/zoom_intrinsics.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization_github_complete/results/wide_angle/0_query_estimated_pose.txt \
/home/ubuntu/Documents/1-pixel/1-jinxia/icme_relocalization_github_complete/results/wide_angle/zoom_render/

/home/ubuntu/Downloads/blender-3.3.1-linux-x64/blender \
-b /home/ubuntu/Documents/1-pixel/blender_demo/reference/reference.blend \
-P /home/ubuntu/Documents/code/视频抽帧/src/blender_rendering/db_depth.py \
-- /home/ubuntu/Documents/dataset/jinxia/wide_angle_0/db_intinsics.txt \
/home/ubuntu/Documents/dataset/jinxia/wide_angle_0/db_pose_200.txt \
/home/ubuntu/Documents/dataset/jinxia/wide_angle_0/depth/
