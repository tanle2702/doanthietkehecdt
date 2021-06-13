import DataCollector as dcM
import WebcamModule as wM
import JoystickModule as jsM
import MotorModule as mM
import cv2
from time import sleep

motor = mM.Motor(23,24,27)

record = 0
maxSpeed = 0.05

while True:
    joyVal = jsM.getCurrentJSValue()
    pwm = joyVal['axis3']*maxSpeed

    if joyVal['share'] ==  1:
        if record == 0: print('Recording..')
        record += 1
        sleep(0.3)
    if record == 1:
        img = wM.getImg(True, 240)
        dcM.saveData(img, pwm)
    elif record == 2:
        dcM.saveLog()
        record = 0

    if joyVal['options'] == 1:
        break

    motor.spin(pwm)
    cv2.waitKey(1)


