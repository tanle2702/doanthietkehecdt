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



vs = cv2.VideoCapture(0)

_, frame = vs.read()
height, width, channel = frame.shape

center = int(width/2)
print('h: {}, w: {}, center: {}'.format(height, width, center))


fps = FPS().start()

while True:
    #read 
    _, frame = cap.read()
    #frame = frame[100:300, 50:250]

    #masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([110,0,0])
    upper = np.array([153,255,255])
    
    mask = cv2.inRange(hsv, lower, upper)

    #find contours
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        centerX = int((x+x+w)/2)
        centerY= int((y+y+h)/2)
        delta = centerX - center
        print(delta)
        cv2.circle(frame, (centerX, centerY), 3 ,(0,0,255), -1)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0) , thickness=4 )
        break

 
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
            ('FPS: ', '{:.2f}'.format(fps.fps())),
            ('Delta: ', '{}'.format(delta)),
            ('Output: ', '{}'.format(speed)),
                ]
        for (i, (k,v)) in enumerate(info):
            text = '{}: {}'.format(k,v)
            cv2.putText(frame, text, (10, H-((i*20)+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        
       
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

