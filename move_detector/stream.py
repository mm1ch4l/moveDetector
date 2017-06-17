'''
Created on 16.06.2017

@author: michal
'''

from flask import Flask, render_template, Response
import time
import cv2
import numpy as np
import detector as d_mod
# from multiprocessing import Process, Lock
import copy
from thread import start_new_thread, allocate_lock

lock = allocate_lock()


app = Flask(__name__)

alarm = False

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        lock.acquire()
        frame = globalJpegFrame 
        lock.release()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +  frame+ b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alarm_feed')
def alarm_feed():
    def generate():
        with open("Wake-up-sounds.mp3", "rb") as mp3:
            data = mp3.read(1024)
            while data:
                yield data
                data = mp3.read(1024)
    return Response(generate(), mimetype="audio/mpeg")
@app.route('/alarm_info')
def alarm_info():
    lock.acquire()
    moveDetection = globalMoveDetection 
    lock.release()
    if(moveDetection):
        return """{ "moveDetected": true}"""
    else:
        return """{ "moveDetected": false}"""

globalMoveDetection = None
globalJpegFrame = None

def detectorThred():
    global globalMoveDetection
    global globalJpegFrame
    detector = d_mod.initDetector()
    print("detector inited")
    while True:
        moveDetection = detector.watch()
        jpegFrame = d_mod.drawDetectorViewJPEG(detector)
        lock.acquire()
        print("new_data")
        globalMoveDetection = moveDetection
        print(moveDetection)
        globalJpegFrame = jpegFrame
        lock.release()
        
if __name__ == '__main__':
    start_new_thread(detectorThred,())
    time.sleep(10)
    app.run(host='0.0.0.0', debug=False)