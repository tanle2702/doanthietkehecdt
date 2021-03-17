import RPi.GPIO as GPIO
from gpiozero import Servo
from time import sleep

class Motor():
    def __init__(self, in1, in2, servo):
        self.in1 = in1
        self.in2 = in2
        self.servo = Servo(servo)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)

    def move(self):
        GPIO.output(self.in1, True)
        GPIO.output(self.in2, False)

    def stop(self):
        GPIO.output(self.in1, False)
        GPIO.output(self.in2, False)

    def steer(self, angle):
        servo.value = angle

def main():
    motor.move()
    sleep(3)
    motor.stop()
    sleep(0.5)
    motor.steer(0.5)
    # sleep(0.5)
    motor.steer(-0.5) 
    # sleep(0.5)
    motor.steer(0)

if __name__ == '__main__':
    motor = Motor(24,23,17)
    main()
    GPIO.cleanup()
