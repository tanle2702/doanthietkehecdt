import RPi.GPIO as GPIO
import bluetooth

#setup
in1 = 24
in2 = 23
servo = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(servo,GPIO.OUT)


#stop everything
GPIO.output(in1,0)
GPIO.output(in2,0)

#set servo duty cycle
pwm = GPIO.pwm(servo, 50)
pwm.start(0)
neutralAngle = 110

def setAngle(angle):
    duty = angle/18+2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    # sleep(1)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)

#bluetooth setup
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(('',bluetooth.PORT_ANY))
server_socket.listen(1)

client_socket, address = server_socket.accept()
#print("Accepted connection from",  address)

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

#loop
while True:
    data = client_socket.recv(1024)
    print("Received %s" % data.decode())
    if data.decode() == "w":
        forward()
    elif data.decode() == "s":
        backward()
    elif data.decode() == "0":
        stop()
    elif data.decode() == "a":
        neutralAngle +=10
        setAngle(neutralAngle)
    elif data.decode() == "d":
        neutralAngle -=10
        setAngle(neutralAngle) 
    elif data.decode() == "n":
        break
stop()
client_socket.close()
server_socket.close()

GPIO.cleanup()
