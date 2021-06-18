import RPi.GPIO as GPIO
import JoystickModule as jM


class Motor():
    def __init__(self, in1, in2, en):
        self.in1 = in1
        self.in2 = in2
        self.en = en
        # pin setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(en, GPIO.OUT)
        
        self.pwm = GPIO.PWM(en, 100)
        self.pwm.start(0)

    def spin(self, speed):
        # speed trong khoang [-1,1]
        # duoi 1 quay phai, nguoc lai quay trai
        if speed < 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(abs(speed * 100))
        else:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            self.pwm.ChangeDutyCycle(speed * 100)


if __name__ == '__main__':
    motor = Motor(23,24,27) 
    while True:
        controllerValue = jM.getCurrentJSValue(name='axis1')
        motor.spin(controllerValue)
        print(controllerValue)


