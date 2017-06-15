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

mixer.init()
mixer.music.load('Wake-up-sounds.mp3')

cam = CamSource(0)
cam.frameDelay = 0



winName = "Movement Indicator"
get_frame_window = "get_frame"
mask_window = "mask"


detector = Detector(cam)
class Mask:
    def __init__(self, size):
        self.mask = np.ones(size, dtype=np.bool)
        self.mask[:100,:100] = False
        self.mouseLeftButtonIsDown = False
        self.mouseRightButtonIsDown = False
        self.penSize = 20
    def applyMask(self,frame):
        return frame * self.mask.astype(frame.dtype)

    def editViaMouse(self,event, x, y, flag, param):
        print(x,y)
        self._decodeMouseEvent(event)
        if(self.mouseLeftButtonIsDown):
            self.addToMask(x, y)
        elif(self.mouseRightButtonIsDown):
            self.removeFromMask(x, y)
    def _decodeMouseEvent(self, event):
        if (cv2.EVENT_LBUTTONDOWN == event):
            self.mouseLeftButtonIsDown = True
        elif(cv2.EVENT_LBUTTONUP == event):
            self.mouseLeftButtonIsDown = False
        elif(cv2.EVENT_RBUTTONDOWN == event):
            self.mouseRightButtonIsDown = True
        elif(cv2.EVENT_RBUTTONUP == event):
            self.mouseRightButtonIsDown = False
    def yPenRange(self, y):
        yMin = max(0, y - self.penSize)
        yMax = min(self.mask.shape[1], y + self.penSize)
        return (yMin, yMax)
    
    def xPenRange(self, x):
        xMin = max(0, x - self.penSize)
        xMax = min(self.mask.shape[0], x + self.penSize)
        return (xMin, xMax)
    
    def addToMask(self,x,y):
        xMin,xMax = self.xPenRange(x)
        yMin,yMax = self.yPenRange(y)
        self.mask[yMin:yMax,xMin:xMax] = True
    def removeFromMask(self,x,y):
        xMin,xMax = self.xPenRange(x)
        yMin,yMax = self.yPenRange(y)
        self.mask[yMin:yMax,xMin:xMax] = False

def mcb(e,x,y,f,p):
    print(x,y)
m = Mask(detector.t0Frame.shape)
cv2.namedWindow(mask_window, cv2.WINDOW_AUTOSIZE)

# cv2.setMouseCallback(mask_window,mcb)
cv2.setMouseCallback(mask_window,m.editViaMouse)
while True:
    
    
    if (detector.watch()):
        print("MOVE DETECTED")
        #mixer.music.play()
    #cv2.imshow(winName, detector.t0Frame)
    #cv2.imshow(get_frame_window, detector.findMovePoints())
    cv2.imshow(mask_window, m.applyMask(detector.t0Frame))
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(winName)
        break
print ("Goodbye")
