import RPi.GPIO as GPIO
from gpiozero import Servo
import bluetooth
from time import sleep
from picamera import PiCamera
NEUTRAL_ANGLE = 0
LEFT_STEER = NEUTRAL_ANGLE + 0.5
RIGHT_STEER = NEUTRAL_ANGLE - 0.5


#setup
in1 = 24
in2 = 23
servo = Servo(17)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
#GPIO.setup(servo,GPIO.OUT)


#stop everything
GPIO.output(in1,0)
GPIO.output(in2,0)

#set servo duty cycle
#pwm = GPIO.PWM(servo, 50)
#pwm.start(0)

#camera setup
camera = PiCamera()

#bluetooth setup
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(('',bluetooth.PORT_ANY))
server_socket.listen(1)
print('Waiting for connection...')

client_socket, address = server_socket.accept()
print("Accepted connection from",  address)

#setup moveset
def forward():
    GPIO.output(in1,1)
    GPIO.output(in2,0)

def backward():
    GPIO.output(in1,0)
    GPIO.output(in2,1)

def stop():
    GPIO.output(in1,0)
    GPIO.output(in2,0)

def setAngle(angle):
    #duty = angle/18+2
    #GPIO.output(servo, True)
    #pwm.ChangeDutyCycle(duty)
    #sleep(0.1)
    #GPIO.output(servo, False)
    #pwm.ChangeDutyCycle(0)
    servo.value = angle 
    print("Steering at " + str(angle))

#camera start recording
camera.start_recording('bluetooth_run.h264')
setAngle(NEUTRAL_ANGLE)

#loop
while True:
    data = client_socket.recv(1024)
    print("Received %s" % data.decode())
    #basic movement forward backward
    if data.decode() == "w":
        forward()
    elif data.decode() == "s":
        backward()
    #movement with steering
    elif data.decode() == "v":
        forward()
        setAngle(LEFT_STEER)
    elif data.decode() == "z":
        forward()
        setAngle(RIGHT_STEER) 
    elif data.decode() == "c":
        backward()
        setAngle(LEFT_STEER)
    elif data.decode() == "x":
        backward()
        setAngle(RIGHT_STEER) 
    #steering only
    elif data.decode() == "a":
        setAngle(LEFT_STEER)
    elif data.decode() == "d":
        setAngle(RIGHT_STEER) 
    elif data.decode() == "0":
        stop()
        setAngle(NEUTRAL_ANGLE)
    elif data.decode() == "n":
        break

stop()
setAngle(NEUTRAL_ANGLE)
camera.stop_recording()
client_socket.close()
server_socket.close()

#GPIO.cleanup()
