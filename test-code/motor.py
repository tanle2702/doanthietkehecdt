import RPi.GPIO as GPIO
from time import sleep

in1 = 8
in2 = 7
#SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)

#RUN
GPIO.output(in1,1)
GPIO.output(in2,0)
