import imutils
import cv2
import numpy as np
from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO


cap = cv2.VideoCapture(0)
cap.set(3,480)
cap.set(4,320)

#servo = Servo(27)
servo = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo, GPIO.OUT)
pwm = GPIO.PWM(servo,50)
pwm.start(0)

def setAngle(angle):
    duty = angle/18+2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.15)

_, frame = cap.read()

frame = frame[100:300, 50:250]
height, width, channel = frame.shape

center = int(width/2)
prev_angle = 90
angle = 90
centerX = int(width/2)

while True:
    #read 
    _, frame = cap.read()
    frame = frame[100:300, 50:250]

    #masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([34,123,0])
    upper = np.array([65,255,183])
    
    mask = cv2.inRange(hsv, lower, upper)

    #find contours
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        centerX = int((x+x+w)/2)
        centerY= int((y+y+h)/2)
        cv2.circle(frame, (centerX, centerY), 3 ,(0,0,255), -1)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0) , thickness=4 )
        break

    if centerX < center -30:
        angle += 2
    elif centerX > center + 30:
        angle -= 2
    if angle > 180:
        angle = 180
    if angle < 0:
        angle = 0

    if not prev_angle == angle:
        setAngle(angle)

    prev_angle = angle

    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
