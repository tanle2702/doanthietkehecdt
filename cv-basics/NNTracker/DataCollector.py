import pandas as pd
import os
from datetime import datetime
import cv2

global imgList, pwmList
countFolder = 0
count = 0
imgList = list()
pwmList = list()

#get current dir
myDir = os.path.join(os.getcwd(), 'DataCollected')

#create a new folder that continues previouse folder count
while os.path.exists(os.path.join(myDir, f'IMG{str(countFolder)}')):
    countFolder += 1
newPath = myDir + '/IMG'+str(countFolder)
os.makedirs(newPath)

print('Created folder ', newPath)


def saveData(img, pwm):
    global imgList, pwmList
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    fileName = os.path.join(newPath, f'Image_{timestamp}.jpg')
    cv2.imwrite(fileName, img)
    imgList.append(fileName)
    pwmList.append(pwm)

def saveLog():
    global imgList, pwmList
    rawData = {'Image': imgList, 'PWM': pwmList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDir, f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log saved')
    print('Total images: ', len(imgList))

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    for x in range(10):
        _, img = cap.read()
        saveData(img, 0.1)
        cv2.waitKey(1)
        cv2.imshow('Image', img)
    saveLog()

