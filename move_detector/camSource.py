'''
Created on 15.06.2017

@author: michal
'''
from videoSource import VideoSource
import cv2
class CamSource(VideoSource):
    '''
    Get frame from Camera
    '''


    def __init__(self, cam_num):
        '''
        Constructor
        '''
        super(CamSource,self).__init__()
        self.cam = cv2.VideoCapture(cam_num)
        
    def _loadFrame(self):
        frame = self.cam.read()[1] 
        return frame