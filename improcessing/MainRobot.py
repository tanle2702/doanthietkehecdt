import CameraModule
from LaneDetectionModule import getLaneCurve
from MotorModule import Motor
import BatteryModule
import cv2
from gpiozero import CPUTemperature

#motor setup

motor = Motor(24,23,17)

def main():
    img = CameraModule.getImg()
    curveVal = getLaneCurve(img, display=1) 
    sens = 1.3
    motor.steer(curveVal)

if __name__ == '__main__':
    motor.move()
    main()
