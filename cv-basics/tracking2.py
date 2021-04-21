import imutils
import cv2
import numpy as np

cap = cv2.VideoCapture(3)
cap.set(3,480)
cap.set(4,320)

while True:
    #read 
    _, frame = cap.read()
    frame = cv2.resize(frame,(640,360))
    frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)

    #masking
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([105,4,0])
    upper = np.array([123,255,150])
    
    mask = cv2.inRange(hsv, lower, upper)

    #find contours
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=4 )
    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
