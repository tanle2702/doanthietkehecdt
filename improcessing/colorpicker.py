import cv2
from os import system, name
import numpy as np
 
frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
 
 
def empty(a):
    pass

def clear():

    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
 
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
 
cap = cv2.VideoCapture('bt_run.mp4')
frameCounter = 0
 
while True:
    frameCounter +=1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        frameCounter=0
 
    _, img = cap.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    clear()
    print("Hmin: " + str(h_min))
    print("Hmax: " + str(h_max))
    print("Smin: " + str(s_min))
    print("Smax: " + str(s_max))
    print("Vmin: " + str(v_min))
    print("Vmax: " + str(v_max))
 
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
 
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
