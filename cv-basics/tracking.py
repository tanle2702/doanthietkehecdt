from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2

# print(cv2.__version__.split('.'))
OPENCV_OBJECT_TRACKERS = { #pip3 install opencv-contrib-python
    'csrt': cv2.TrackerCSRT_create,
    'kcf': cv2.TrackerKCF_create,
    # 'boosting': cv2.TrackerBoosting_create,
    'mil': cv2.TrackerMIL_create,
    # 'tld': cv2.TrackerTLD_create,
    # 'medianflow': cv2.TrackerMedianFlow_create,
    # 'mosse': cv2.TrackerMOSSE_create
        }
initBB = None

tracker =  OPENCV_OBJECT_TRACKERS['csrt']()

vs = cv2.VideoCapture(3)

fps = None

while True:
    _, frame = vs.read()
    if frame is None:
       break

    frame = imutils.resize(frame, width=500)
    (H,W) = frame.shape[:2]
    
    if initBB is not None:
        success, box = tracker.update(frame)

        if success:
            (x,y,w,h) = [int(v) for v in box]
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),3)

        fps.update()
        fps.stop()

        info = [
            ('Tracker: ', 'kcf'),
            ('Success: ', 'Yes' if success else 'No'),
            ('FPS: ', '{:.2f}'.format(fps.fps())),
                ]
        for (i, (k,v)) in enumerate(info):
            text = '{}: {}'.format(k,v)
            cv2.putText(frame, text, (10, H-((i*20)+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
       
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        initBB = cv2.selectROI("Frame", frame)
        tracker.init(frame, initBB)
        fps = FPS().start()

    if key == ord('q'):
        break

