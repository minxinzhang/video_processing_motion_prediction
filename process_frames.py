import math
import cv2
import numpy as np
import os

if not os.path.exists('./output_frames/'):
        os.makedirs('./output_frames/')
block_len = 10
global foreground_threshold
global knn_threshold
global source_frame
global target_frame
t_min = 400
t_max = 1000
block_centers = []
global k
global y_size
global x_size

def calculate_knn_threshold():
    global knn_threshold
    knn_threshold = 5
    print('knn_threshold= ', knn_threshold)
    return 

def generate_block_centers(x_size, y_size):
    y_num = math.floor(y_size/block_len)
    x_num = math.floor(x_size/block_len)
    for y_idx in range(y_num):
        for x_idx in range(x_num):
            global k
            k = int((block_len-1)/2)
            block_centers.append((k + x_idx * block_len,k + y_idx * block_len))
    return

def sqrssd(s_x,s_y,t_x,t_y):
    sum = 0
    k = int((block_len-1)/2)
    for y_offset in range(-k,k+1):
        for x_offset in range(-k,k+1):
             for color_idx in range(3):
                 square_difference = ((int(source_frame[s_y + y_offset][s_x + x_offset][color_idx]) - int(target_frame[t_y + y_offset][t_x + x_offset][color_idx])) ** 2) 
                 sum += square_difference
    return math.sqrt(sum)

def arrowdraw(img, x1, y1, x2, y2): 
    radians = math.atan2(x1-x2, y2-y1)
    x11 = 0
    y11 = 0
    x12 = -3
    y12 = -3

    u11 = 0
    v11 = 0
    u12 = 3
    v12 = -3
    
    x11_ = x11*math.cos(radians) - y11*math.sin(radians) + x2
    y11_ = x11*math.sin(radians) + y11*math.cos(radians) + y2

    x12_ = x12 * math.cos(radians) - y12 * math.sin(radians) + x2
    y12_ = x12 * math.sin(radians) + y12 * math.cos(radians) + y2
    
    u11_ = u11 * math.cos(radians) - v11 * math.sin(radians) + x2
    v11_ = u11 * math.sin(radians) + v11 * math.cos(radians) + y2

    u12_ = u12 * math.cos(radians) - v12 * math.sin(radians) + x2
    v12_ = u12 * math.sin(radians) + v12 * math.cos(radians) + y2
    if (x1==x2 and y1 == y2):
        img = cv2.line(img,(x1,y1),(x2,y2),(255,255,255),1)
    else:
        img = cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 1)
        img = cv2.line(img, (int(x11_), int(y11_)), (int(x12_), int(y12_)), 
        (255, 255, 255), 1)
        img = cv2.line(img, (int(u11_), int(v11_)), (int(u12_), int(v12_)), 
        (255, 255, 255), 1)
    
    return img

def calculate_foreground_threshold(gray_image):
    res = []
    for (center_x,center_y) in block_centers:
        sum = 0 
        for y_offset in range(-k,k+1):
            for x_offset in range(-k,k + 1):
                sum += gray_image[center_y + y_offset][center_x + x_offset]
        res.append(sum)
    res = np.array(res)
    return np.mean(res) + 4 * np.std(res)

def within_boundary(x,y):
    if (x-k >= 0 and x+k <= x_size and y-k >= 0 and y+k <= y_size):
        return True
    return False

def search(s_x, s_y):
    #dimond search
    min_sqrssd = t_max
    min_t_pair = (s_x,s_y)
    for n in range(0, knn_threshold):
        #dimond search iterations
        invalid_iteration = True
        for x_offset in range(-n, n + 1):
            y_diff = n - abs(x_offset)
            if y_diff == 0:
                y_range = [0]
            else:
                y_range = [-y_diff,y_diff]
            for y_offset in y_range:
                t_x = s_x + x_offset * block_len
                t_y = s_y + y_offset * block_len
                if within_boundary(t_x,t_y):
                    val = sqrssd(s_x, s_y, t_x, t_y)
                    if (val > t_min and val < t_max):
                        if val < min_sqrssd:
                            min_sqrssd = val
                            min_t_pair = (t_x,t_y)
                            invalid_iteration = False
        # early termination
        if invalid_iteration and min_sqrssd < t_max:
            return min_t_pair
    return min_t_pair

def process():
    count = 0
    arrowed_frame = source_frame
    diff = cv2.absdiff(source_frame,target_frame)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for (center_x, center_y) in block_centers:
        sum = 0 
        for y_offset in range(-k, k + 1):
            for x_offset in range(-k, k + 1):
                sum += gray_diff[center_y + y_offset][center_x + x_offset]
        if sum > foreground_threshold:
            (t_x,t_y) = search(center_x, center_y)
            arrowdraw(arrowed_frame,center_x,center_y,t_x,t_y) 
    return arrowed_frame

process_frame = 1
source_frame = cv2.imread('./test_frames/frame%d.tif' % process_frame)
y_size = source_frame.shape[0]
x_size = source_frame.shape[1]
generate_block_centers(x_size, y_size)
calculate_knn_threshold()
target_frame = cv2.imread('./test_frames/frame%d.tif' % (process_frame + 1))
diff = cv2.absdiff(source_frame,target_frame)
gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
foreground_threshold = calculate_foreground_threshold(gray_diff)
print('source threshold=', foreground_threshold)
# cv2.imwrite('./tuning/blocksize%dTmin%dTmax%d.tif'%(block_len,t_min,t_max),process())
cv2.imwrite('./output_frames/output%d.tif'%process_frame,process())
for i in range(2,752):
    source_frame = cv2.imread('./test_frames/frame%d.tif' % i)
    target_frame = cv2.imread('./test_frames/frame%d.tif'%(i + 1))
    cv2.imwrite('./output_frames/output%d.tif'%i,process())

