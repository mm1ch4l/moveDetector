'''
Created on 15.06.2017

@author: michal
'''
import cv2
import time
class VideoSource(object):
    '''
    Source of images
    '''


    def __init__(self ):
        '''
        Constructor
        '''
        self.frameT = 1 #s
        self.lastFrameT = 0
        self.bilateralFilter_D = 10
    
    def getFrame(self):
        now = time.time()
        timeToWait = self.frameT - (now - self.lastFrameT)
        self.lastFrameT = now
        if timeToWait > 0:
            time.sleep(timeToWait)
        frame = self._loadFrame()
        return self._filter(frame)
        
    def _loadFrame(self):
        raise NotImplementedError
    
    def _filter(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        #frame = cv2.bilateralFilter(frame, self.bilateralFilter_D, 75, 75)
        return frame