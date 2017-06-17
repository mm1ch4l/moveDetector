'''
Created on 16.06.2017

@author: michal
'''

from flask import Flask, render_template, Response
import time
import cv2
import numpy as np
from camSource import CamSource
from detector import Detector
from maskManager import MaskManager

def initDetector():
    cam = CamSource(0)
    time.sleep(1)
    m = MaskManager(cam.getFrame().shape)
    detector = Detector(cam,m )
    return detector

def drawDetectorViewJPEG(detector):
    frame = cv2.cvtColor(detector.t2Frame, cv2.COLOR_GRAY2RGB)
    frame = detector.mask.drawMask(frame)
    frame = detector.drawEvents(frame)
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()
app = Flask(__name__)

alarm = False

@app.route('/')
def index():
    return render_template('index.html')

def gen(detector):
    while True:
        global alarm
        alarm = detector.watch()
        frame = drawDetectorViewJPEG(detector)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +  frame+ b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    d = initDetector()
    return Response(gen(d),
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
    return """{ "moveDetected": true}"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)