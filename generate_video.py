import math
import cv2
import numpy as np
frame_counter = 1
img = cv2.imread('./output_frames/' + 'output%d.tif' % frame_counter)
out = cv2.VideoWriter('./SID490210055_Ass1a.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 24, (int(img.shape[1]), int(img.shape[0])))
while(1):
    img = cv2.imread('./output_frames/' + 'output%d.tif' % frame_counter)
    if img is None:
        print('No more frames to be loaded')
        break
    out.write(img)
    frame_counter += 1
out.release()
cv2.destroyAllWindows()