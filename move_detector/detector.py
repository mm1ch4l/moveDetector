'''
Created on 15.06.2017

@author: michal
'''

import cv2
import time
import numpy as np
from camSource import CamSource

from maskManager import MaskManager
def initDetector():
    cam = CamSource(0)
#     cam = CamSource("http://192.168.1.106:8080/video")
    time.sleep(3)
    m = MaskManager(cam.getFrame().shape)
    detector = Detector(cam,m )
    return detector

def drawDetectorViewJPEG(detector):
    frame = cv2.cvtColor(detector.t2Frame, cv2.COLOR_GRAY2RGB)
    frame = detector.mask.drawMask(frame)
    frame = detector.drawEvents(frame)
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

class Detector(object):
    '''
    Tetect moves form cameras
    '''


    def __init__(self, videoSource, mask):
        '''
        Constructor
        '''
        self.vs = videoSource
        self.t0Frame = self.vs.getFrame()
        self.t1Frame = self.vs.getFrame()
        self.t2Frame = self.vs.getFrame()
        self.moveMapFilterSize = 10
        self.moveMapTreshold = 3
        self.detectionTheshold = 100
        self.mask = mask
        self.detectionMap = None
        self.moveEventsTime = []
        self.maxTimeEventsHistory = 20
        self.eventNumTreshold = 15
        
    def _diffImg(self):
        d1 = cv2.absdiff(self.t2Frame, self.t1Frame)
        d2 = cv2.absdiff(self.t1Frame, self.t0Frame)
        return cv2.bitwise_and(d1, d2)
    
    def findMovePoints(self):
        moveMap = self._diffImg()
        moveMap = cv2.bilateralFilter(moveMap, self.moveMapFilterSize, 75, 75)
        return self.mask.applyMask(moveMap)
    
    def isEventDetected(self, moveMap):
        self.detectionMap = cv2.inRange(moveMap, self.moveMapTreshold, 255)
        if(cv2.countNonZero(self.detectionMap)> self.detectionTheshold):
            return True
        else:
            return False
    def isMoveDetected(self, moveMap):
        if(self.isEventDetected(moveMap)):
            self.moveEventsTime.append(time.time())
            self._deleteOldEvents()
            if len(self.moveEventsTime) >= self.eventNumTreshold:
                return True
        return False
            
    def _deleteOldEvents(self):
        now = time.time()
        firstExpire =None
        for e in self.moveEventsTime:
            if (now - self.maxTimeEventsHistory > e):
                firstExpire = self.moveEventsTime.index(e)
                break
        if firstExpire is not None:    
            self.moveEventsTime = self.moveEventsTime[:firstExpire]
    
    def getNewFrame(self):
        self.t0Frame = self.t1Frame
        self.t1Frame = self.t2Frame
        self.t2Frame = self.vs.getFrame()
            
    def watch(self):
        self.getNewFrame()
        moveMap = self.findMovePoints()
        return self.isMoveDetected(moveMap)
    
    def drawEvents(self,frame):
        frame[:,:,1] =  np.where(self.detectionMap, 0, frame[:,:,1])
        frame[:,:,0] =  np.where(self.detectionMap, 0, frame[:,:,0])
        return frame
        