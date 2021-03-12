from picamera import PiCamera
from time import sleep
#setup
camera = PiCamera()
#camera.resolution = (1920,1080)

#run
camera.start_preview()
camera.capture('/home/pi/still.jpg')
sleep(5)
camera.stop_preview()

