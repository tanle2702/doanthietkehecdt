from picamera import PiCamera

with PiCamera() as camera:
#    camera.resolution = (1920,1080)
    camera.start_recording('capture_video_3s.h264', resize=(1024,768))
    camera.wait_recording(3)
    camera.stop_recording()
