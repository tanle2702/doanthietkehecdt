import RPi.GPIO as GPIO
from time import sleep
import sys

#setup 
servo = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo, GPIO.OUT)

pwm = GPIO.PWM(servo, 50)
#reset pwm
pwm.start(0)

#run
def setAngle(angle):
    duty = angle/18+2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
#110 deg is straight
setAngle(int(sys.argv[1]))

pwm.stop()
GPIO.cleanup()
