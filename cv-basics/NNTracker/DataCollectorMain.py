import DataCollector as dcM
import JoystickModule as jsM
import MotorModule as mM
import cv2
from time import sleep

motor = mM.Motor(23,24,27)

record = 0

while True:
    joyVal = jsM.getCurrentJSValue()
    pwm = joyVal['axis1']

    if joyVal['share'] ==  1:
        if record == 0: print('Recording..')
        record += 1
        sleep(0.3)
    if record == 1:
        img = wM.getImg(True, size=[240,120])
        dcM.saveData(img, steering)
    elif record == 2:
        dcM.saveLog()
        record = 0
    motor.spin(pwm)
    cv2.waitKey(1)


