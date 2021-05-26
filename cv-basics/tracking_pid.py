from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
from time import sleep
import numpy as np
import cv2
from simple_pid import PID
import RPi.GPIO as io

#pid initialization
pid = PID(0.25,1,2, setpoint=0)

#motor initialization
in3 = 23
in4 = 24
enB = 22

io.setmode(io.BCM)
io.setup(in3, io.OUT)
io.setup(in4, io.OUT)
io.setup(enB, io.OUT)

pwm = io.PWM(enB, 100)
pwm.start(0)


def moveLeft(speed):
    io.output(in3, io.HIGH)
    io.output(in4, io.LOW)
    pwm.ChangeDutyCycle(speed)

def moveRight(speed):
    io.output(in3, io.LOW)
    io.output(in4, io.HIGH)
    pwm.ChangeDutyCycle(speed)


OPENCV_OBJECT_TRACKERS = { #pip3 install opencv-contrib-python
    'csrt': cv2.TrackerCSRT_create,
    'kcf': cv2.TrackerKCF_create,
    # 'boosting': cv2.TrackerBoosting_create,
    'mil': cv2.TrackerMIL_create,
    # 'tld': cv2.TrackerTLD_create,
    # 'medianflow': cv2.TrackerMedianFlow_create,
    # 'mosse': cv2.TrackerMOSSE_create
        }
initBB = None

tracker =  OPENCV_OBJECT_TRACKERS['csrt']()

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

    (H,W) = frame.shape[:2]
    
    if initBB is not None:
        success, box = tracker.update(frame)

        if success:
            (x,y,w,h) = [int(v) for v in box]
            centerX = int(x+w/2)
            centerY = int(y+h/2)
            delta = int(center - centerX)
            print('cX: {}, cY: {}, delta: {}'.format(centerX,centerY, delta))
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),3)
            cv2.circle(frame, (centerX, centerY), 5, (0,0,255), -1)

            #OUTPUT TO MOTOR
            speed = pid(delta)
            
            #constrain
            if speed > 100:
                speed = 100
            if speed < -100:
                speed = -100

            #output
            if delta < 0:
                moveLeft(abs(speed))
            if delta > 0:
                moveRight(abs(speed))

            

 

        fps.update()
        fps.stop()

        info = [
            ('Tracker: ', 'csrt'),
            ('Success: ', 'Yes' if success else 'No'),
            ('FPS: ', '{:.2f}'.format(fps.fps())),
            ('Delta: ', '{}'.format(delta)),
            ('Output: ', '{}'.format(speed)),

                ]
        for (i, (k,v)) in enumerate(info):
            text = '{}: {}'.format(k,v)
            cv2.putText(frame, text, (10, H-((i*20)+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        
       
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        initBB = cv2.selectROI("Frame", frame)
        tracker.init(frame, initBB)
        fps = FPS().start()

    if key == ord('q'):
        break

