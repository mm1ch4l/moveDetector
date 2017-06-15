'''
Created on 15.06.2017

@author: michal
'''

import cv2
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
    
    def _diffImg(self):
        d1 = cv2.absdiff(self.t2Frame, self.t1Frame)
        d2 = cv2.absdiff(self.t1Frame, self.t0Frame)
        return cv2.bitwise_and(d1, d2)
    
    def findMovePoints(self):
        moveMap = self._diffImg()
        moveMap = cv2.bilateralFilter(moveMap, self.moveMapFilterSize, 75, 75)
        return self.mask.applyMask(moveMap)
    
    def isMoveDetected(self, moveMap):
        self.detectionMap = cv2.inRange(moveMap, self.moveMapTreshold, 255)
        if(cv2.countNonZero(self.detectionMap)> self.detectionTheshold):
            return True
        else:
            return False
    
    def getNewFrame(self):
        self.t0Frame = self.t1Frame
        self.t1Frame = self.t2Frame
        self.t2Frame = self.vs.getFrame()
            
    def watch(self):
        self.getNewFrame()
        moveMap = self.findMovePoints()
        return self.isMoveDetected(moveMap)