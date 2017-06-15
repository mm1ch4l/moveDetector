'''
Created on 15.06.2017

@author: michal
'''
import cv2
import time
from pygame import mixer
from camSource import CamSource
def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

mixer.init()
mixer.music.load('Wake-up-sounds.mp3')

cam = CamSource(0)
cam.frameDelay = 0.1

def mouseCallBack(event,x,y,flags,params):
    if(event == cv2.EVENT_LBUTTONDOWN):
        print(x,y)


winName = "Movement Indicator"
get_frame_window = "get_frame"
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(get_frame_window, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(get_frame_window, mouseCallBack)
# Read three images first:
t_minus = cam.getFrame()
t = cam.getFrame()
t_plus = cam.getFrame()



while True:
    diff = diffImg(t_minus, t, t_plus)
    diff = cv2.bilateralFilter(diff, 10, 75, 75)
    diff = cv2.inRange(diff, 3 , 255)
    cv2.imshow(winName, diff)
    non_zero = cv2.countNonZero(diff) 
    if (non_zero > 50):
        print(non_zero)
        #mixer.music.play()


    # Read next image
    new_frame = cam.getFrame()
    cv2.imshow(get_frame_window, new_frame)
    t_minus = t
    t = t_plus
    t_plus = new_frame  # cv2.cvtColor(new_frame, cv2.COLOR_RGB2GRAY)
    
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break
print ("Goodbye")
