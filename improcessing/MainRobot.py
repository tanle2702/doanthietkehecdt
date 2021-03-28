import CameraModule
from LaneDetectionModule import getLaneCurve
from MotorModule import Motor
import BatteryModule
import cv2
from gpiozero import CPUTemperature
from time import sleep

#motor setup

motor = Motor(24,23,27)

def main():
    img = CameraModule.getImg()
    curveVal = getLaneCurve(img, display=0) 
    sens = 1
    motor.steer(-sens*curveVal)

if __name__ == '__main__':
    motor.move()
    while True:
    if checkEndOfLane(warped, wT, hT) == False:
        curveRaw = 0
        motor.stop()
        motor.steer(curveRaw)
        cv2.waitKey(1)
    else:
        main()
        cv2.waitKey(1)

