'''
Created on 15.06.2017

@author: michal
'''
import cv2
import time
from pygame import mixer
def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

mixer.init()
mixer.music.load('Wake-up-sounds.mp3')

cam = cv2.VideoCapture(1)

def mouseCallBack(event,x,y,flags,params):
    if(event == cv2.EVENT_LBUTTONDOWN):
        print(x,y)

def get_frame(cam):
    frame = cam.read()[1]
    frame_num = 10
    time.sleep(0.1)
    # for i in range(frame_num):
    #  base_factor = 1/frame_num * (frame_num- i)
    #  new_factor = 1 - base_factor
    #  frame = cv2.addWeighted(frame, base_factor,  cam.read()[1], new_factor , 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frame = cv2.bilateralFilter(frame, 9, 75, 75)
    return frame
winName = "Movement Indicator"
get_frame_window = "get_frame"
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(get_frame_window, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(get_frame_window, mouseCallBack)
# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)



while True:
    diff = diffImg(t_minus, t, t_plus)
    diff = cv2.inRange(diff, 10 , 255)
    cv2.imshow(winName, diff)
    non_zero = cv2.countNonZero(diff) 
    if (non_zero > 50):
        print(non_zero)
        #mixer.music.play()


    # Read next image
    new_frame = get_frame(cam)
    cv2.imshow(get_frame_window, new_frame)
    t_minus = t
    t = t_plus
    t_plus = new_frame  # cv2.cvtColor(new_frame, cv2.COLOR_RGB2GRAY)
    
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break
print ("Goodbye")
