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

# cam = CamSource("http://192.168.1.106:8080/video")
cam = CamSource(0)
time.sleep(1)

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
    
    if (detector.watch()):
        counter +=1
        print("MOVE DETECTED: " + str(counter))
        mixer.music.play()
#     cv2.imshow(winName, vid.read()[1])
    frame = cv2.cvtColor(detector.t2Frame, cv2.COLOR_GRAY2RGB)
    frame = detector.mask.drawMask(frame)
    frame = detector.drawEvents(frame)
#     cv2.imshow(get_frame_window, detector.detectionMap)
    cv2.imshow(mask_window, frame)
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break
m.save()
print ("Goodbye")
