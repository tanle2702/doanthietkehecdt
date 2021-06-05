from RPi.GPIO import GPIO
import JoystickModule as jM


class Motor():
    def __init__(self, in1, in2, en):
        self.in1 = in1
        self.in2 = in2
        self.en = en
        # pin setup
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        self.pwm = GPIO.PWM(en, 100)
        self.pwm.start(0)

    def spin(self, speed):
        # speed trong khoang [-1,1]
        # duoi 1 quay phai, nguoc lai quay trai
        if speed < 0:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            self.pwm.ChangeDutyCycle(en, speed * 100)
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(en, speed * 100)


if __name__ == '__main__':
    controllerValue = jM.getCurrentJSValue(name='axis2')
    motor = Motor(23,24,22) 
    motor.spin(controllerValue)

