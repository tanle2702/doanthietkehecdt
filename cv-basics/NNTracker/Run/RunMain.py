import cv2
import numpy as np
from tensorflow.keras.models import load_model

import WebcamModule as wM
import MotorModule as mM

###################################
steeringSens = 1
motor = mM.Motor(23,24,27)
model = load_model('model.h5')
###################################

def preProcess(img): # do the same as the utlis module
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3,3), 0)
    img = cv2.resize(img, (240,180))
    img = img/255
    return img

while True:
    img = wM.getImg(True)
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    steering = float(model.predict(img))
    print(steering)
    motor.spin(steering)
