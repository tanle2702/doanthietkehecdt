import imutils
import cv2
import numpy as np
from gpiozero import Servo

cap = cv2.VideoCapture(4)
cap.set(3,480)
cap.set(4,320)

servo = Servo(27)

_, frame = cap.read()
height, width, channel = frame.shape

center = int(width/2)
print('h: {}, w: {}, center: {}'.format(height, width, center))



while True:
    #read 
    _, frame = cap.read()
    # frame = cv2.resize(frame,(640,360))
    # frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)

    #masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([105,4,0])
    upper = np.array([123,255,150])
    
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
    delta = centerX - center
    print('delta: {}'.format(delta))
    angle = delta/100
    if angle > 1:
        angle = 1
    if angle < -1:
        angle = -1
    servo.value = angle
    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
