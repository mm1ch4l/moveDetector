'''
Created on 15.06.2017

@author: michal
'''
import time
import cv2
import numpy as np
from pygame import mixer
from camSource import CamSource
from detector import Detector
from maskManager import MaskManager
mixer.init()
mixer.music.load('Wake-up-sounds.mp3')

cam = CamSource(0)
cam.frameDelay = 0



winName = "Movement Indicator"
get_frame_window = "get_frame"
mask_window = "mask"


m = MaskManager(cam.getFrame().shape)
detector = Detector(cam,m )
cv2.namedWindow(mask_window, cv2.WINDOW_AUTOSIZE)

# cv2.setMouseCallback(mask_window,mcb)
cv2.setMouseCallback(mask_window,m.editViaMouse)
counter = 0
while True:
    counter +=1
    
    if (detector.watch()):
        print("MOVE DETECTED:".format(counter))
        mixer.music.play()
    #cv2.imshow(winName, detector.t0Frame)
    cv2.imshow(get_frame_window, detector.detectionMap)
    cv2.imshow(mask_window, m.applyMask(detector.t0Frame))
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break
print ("Goodbye")
