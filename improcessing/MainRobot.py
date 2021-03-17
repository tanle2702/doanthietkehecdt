import CameraModule
from LaneDetectionModule import getLaneCurve
from MotorModule import Motor
import BatteryModule
import cv2
from gpiozero import CPUTemperature

#motor setup

motor = Motor(24,23,27)

def main():
    img = CameraModule.getImg()
    curveVal = getLaneCurve(img, display=2) 
    sens = 1
    motor.steer(-sens*curveVal)

if __name__ == '__main__':
    while True:
        motor.move()
        main()
        cv2.waitKey(1)

