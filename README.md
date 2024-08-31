# 个人项目介绍
此项目采用OpenCV和numpy库来进行视频处理，预测视频中物体的移动相位。
## `extract_frames.py`
对源视频逐帧采样
## `process_frames.py`
核心算法是将图像像素合并成某大小（针对不同视频需要调参）的网格，对比前帧某网格和后帧临近几个网格的像素平均标准差，从而预测物体某个部位的运动方式。
# How to run the code
## 1. extract frames from the original video
`python extract_frames.py`
## 2. process the frames
`python process_frames.py`
## 3. convert processed frames to a video
`python generate_video.py`
