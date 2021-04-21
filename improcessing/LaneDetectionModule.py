import cv2
import numpy as np
from utlis import *
from BatteryModule import INA219
from gpiozero import CPUTemperature

curveList = []
avgCurveN = 10
cpu = CPUTemperature()
ina219 = INA219(addr=0x42)

def getLaneCurve(img, display=2): # 0 for not display, 1 for the result, 2 for the complete pipeline
    #battery percentage
    bus_voltage = ina219.getBusVoltage_V()
    p = (bus_voltage-6)/2.4*100
    if p>100: p = 100
    if p<0: p = 0

    imgCopy = img.copy()
    imgResult = img.copy()
    #STEP 1 THRESHOLDING
    thresh = thresholding(img)

    #STEP 2 WARPING
    hT, wT, c = img.shape
    pts = getPoints(199,264,100,322, wT, hT)
    warped = warpImg(thresh,pts,wT,hT) 

    #STEP 3 LANE DETECTION

    # CHECKING FOR END OF LINE
    curveAveragePoint, _ = getHistogram(warped.copy(), display=True, noise_gate=0.9,region=1)
    midPoint, imgHistogram = getHistogram(warped.copy(), display=True,region=3)
    curveRaw = curveAveragePoint - midPoint
    if checkEndOfLane(warped, wT, hT) == False:
        curveRaw = 0

    #STEP 4 AVERAGING
    curveList.append(curveRaw)
    if len(curveList) > avgCurveN:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    # NORMALIZATION
    curve_norm = curve/100
    #if curve_norm > 1: curve_norm=1
    #if curve_norm < -1: curve_norm=-1




    #STEP 5 DISPLAYING RESULT
    if display != 0:
        imgInvWarp = warpImg(warped, pts, wT, hT,inv = True)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3,0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        midY = 450
        cv2.putText(imgResult,"Curve: " + str(curve_norm),(30,30),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
        cv2.putText(imgResult,"Temp: " + str(cpu.temperature),(30,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
        cv2.putText(imgResult,"Battery percentage: " + str(p) + "%" ,(30,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
        cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                     (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
        imgStacked = stackImages(0.7,([img,thresh,warped],
                                          [_,imgHistogram,imgResult]))
        cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
        cv2.imshow('Result',imgResult)
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('warped', warped)
    # cv2.imshow('histogram', _)
    # cv2.imshow('histogram 1/4', imgHistogram)
    return curve_norm

if __name__ == '__main__':
    cap = cv2.VideoCapture('output.avi')
    framecounter = 0
    while True:
        framecounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == framecounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            framecounter = 0

        ret, frame = cap.read()
        curve = getLaneCurve(frame, display=2)
        #warped = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)
        #imgHistogram = cv2.cvtColor(imgHistogram, cv2.COLOR_GRAY2BGR)
        #hStack = np.hstack([frame, warped, imgHistogram])
        #cv2.imshow('', frame)
        cv2.waitKey(1)
