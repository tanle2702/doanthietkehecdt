import cv2
from imutils import resize
cap = cv2.VideoCapture(0)

def getImg(display=False, width=480):
    _, img = cap.read()
    img = resize(img, width=width)
    if display: 
        cv2.imshow('IMG', img)
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)
        cv2.waitKey(1)
