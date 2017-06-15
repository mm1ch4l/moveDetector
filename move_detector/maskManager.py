'''
Created on 15.06.2017

@author: michal
'''
import numpy as np
import cv2
class MaskManager:
    def __init__(self, size):
        self.mask = np.ones(size, dtype=np.bool)
        self.mask[:100,:100] = False
        self.mouseLeftButtonIsDown = False
        self.mouseRightButtonIsDown = False
        self.penSize = 20
    def applyMask(self,frame):
        return frame * self.mask.astype(frame.dtype)

    def editViaMouse(self,event, x, y, flag, param):
        self._decodeMouseEvent(event)
        if(self.mouseLeftButtonIsDown):
            self.removeFromMask(x, y)
        elif(self.mouseRightButtonIsDown):
            self.addToMask(x, y)
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
        yMin = max(1, y - self.penSize)
        yMax = min(self.mask.shape[0], y + self.penSize)
        return (yMin, yMax)
    
    def xPenRange(self, x):
        xMin = max(1, x - self.penSize)
        xMax = min(self.mask.shape[1], x + self.penSize)
        return (xMin, xMax)
    
    def addToMask(self,x,y):
        xMin,xMax = self.xPenRange(x)
        yMin,yMax = self.yPenRange(y)
        self.mask[yMin:yMax,xMin:xMax] = True
    def removeFromMask(self,x,y):
        xMin,xMax = self.xPenRange(x)
        yMin,yMax = self.yPenRange(y)
        self.mask[yMin:yMax,xMin:xMax] = False
