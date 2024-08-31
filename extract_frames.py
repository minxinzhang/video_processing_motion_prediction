import sys
import os
import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
import math

path_to_video = 'monkey.avi'

# Capture Video and represent it as a object
cap = cv2.VideoCapture(path_to_video)
# Check whether video is captured correctly by cv2
if not cap.isOpened():
    print('{} not opened'.format(path_to_video))
    sys.exit(1)
# Use cv2 to fetch three important variables
time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# Use for loop to have access to video frame by frame
frame_count = 0
if not os.path.exists('./test_frames/'):
        os.makedirs('./test_frames/')
while(1):
    return_flag, frame = cap.read()  
    if not return_flag:
        # return_flag=False when the video ends
        print('Video Reach End')
        break
        
    
    frame_count += 1
    
    cv2.imwrite('./test_frames/frame%d.tif' % frame_count, frame)
        

    
    if cv2.waitKey(30) & 0xff == ord('q'):
        break
# Securely release video and close windows
cap.release()
cv2.destroyAllWindows()