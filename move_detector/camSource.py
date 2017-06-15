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
        self.cam = cv2.VideoCapture(cam_num)
        
    def __loadFrame(self):
        frame = self.cam.read()[1] 
        return frame