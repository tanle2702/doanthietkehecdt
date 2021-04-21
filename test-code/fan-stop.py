import RPi.GPIO as GPIO
from time import sleep

in3 = 8
in4 = 7
#SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

#RUN
GPIO.output(in3,0)
GPIO.output(in4,0)


