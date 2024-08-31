# 个人项目介绍
此项目采用OpenCV和numpy库来进行视频处理，预测视频中物体的移动相位。
## `extract_frames.py`
对源视频逐帧采样
## `process_frames.py`
算法是将图像像素合并成某大小（针对不同视频需要调参）的网格，对比前帧某网格和后帧临近几个网格的像素平均标准差，从而预测物体某个部位的运动方式。
优化算力方面，`calculate_foreground_threshold(gray_image)`函数会预先处理视频第一帧的各个网格。从统计学角度预设了目标网格的上下限值，忽略了非目标物体网格与在KNN算法和菱形搜索的时候自动忽略偏差太大网格的比对计算，加快了每一帧的处理。每一帧结束后给图片添加位移矢量的标记导出成处理完成的一帧。
## `generate_video.py`
将所有处理完的帧数合并成视频，每秒帧数可以微调，压缩视频大小。最后处理完的效果可以参考视频`output.mp4`。
# How to run the code
## 1. extract frames from the original video
`python extract_frames.py`
## 2. process the frames
`python process_frames.py`
## 3. convert processed frames to a video
`python generate_video.py`
