from imutils.video import VideoStream
from imutils.video import FPS
from gpiozero import Servo
import imutils
import time
import numpy as np
import cv2

servo = Servo(27)
servo.value = 0


# print(cv2.__version__.split('.'))
OPENCV_OBJECT_TRACKERS = { #pip3 install opencv-contrib-python
    #'csrt': cv2.TrackerCSRT_create,
    'kcf': cv2.TrackerKCF_create,
    # 'boosting': cv2.TrackerBoosting_create,
    # 'mil': cv2.TrackerMIL_create,
    # 'tld': cv2.TrackerTLD_create,
    # 'medianflow': cv2.TrackerMedianFlow_create,
    # 'mosse': cv2.TrackerMOSSE_create
        }
initBB = None

tracker =  OPENCV_OBJECT_TRACKERS['kcf']()

vs = cv2.VideoCapture(0)

_, frame = vs.read()
height, width, channel = frame.shape

center = int(width/2)
print('h: {}, w: {}, center: {}'.format(height, width, center))


fps = None

while True:
    _, frame = vs.read()
    if frame is None:
       break

    # frame = imutils.resize(frame, width=500)
    (H,W) = frame.shape[:2]
    
    if initBB is not None:
        success, box = tracker.update(frame)

        if success:
            (x,y,w,h) = [int(v) for v in box]
            cX = int(x+w/2)
            cY = int(y+h/2)
            delta = int((center - cX)/100)
            print('cX: {}, cY: {}, delta: {}'.format(cX,cY, delta))
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),3)
            cv2.circle(frame, (cX, cY), 5, (0,0,255), -1)

        fps.update()
        fps.stop()

        info = [
            ('Tracker: ', 'csrt'),
            ('Success: ', 'Yes' if success else 'No'),
            ('FPS: ', '{:.2f}'.format(fps.fps())),
            ('Delta: ', '{}'.format(center-cX)),
                ]
        for (i, (k,v)) in enumerate(info):
            text = '{}: {}'.format(k,v)
            cv2.putText(frame, text, (10, H-((i*20)+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        
        if delta > 1:
            delta = 1
        if delta < -1:
            delta = -1

        servo.value = delta  
       
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        initBB = cv2.selectROI("Frame", frame)
        tracker.init(frame, initBB)
        fps = FPS().start()

    if key == ord('q'):
        break

