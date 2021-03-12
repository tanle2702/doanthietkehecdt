from picamera import PiCamera
import RPi.GPIO as GPIO

#setup
in1 = 24
in2 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

#run
with PiCamera() as camera:
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    camera.start_recording('sample_run.h264')
    camera.wait_recording(5)
    camera.stop_recording()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

