import CameraModule
from LaneDetectionModule import getLaneCurve
from utlis import checkEndOfLane
from MotorModule import Motor
import BatteryModule
import cv2
from gpiozero import CPUTemperature
from time import sleep

#motor setup

motor = Motor(24,23,27)

def main():
    img = CameraModule.getImg()
    curveVal = getLaneCurve(img, display=2) 
    sens = 1
    motor.steer(-sens*curveVal)

if __name__ == '__main__':
    motor.move()
    while True:
        main()
        cv2.waitKey(1)

