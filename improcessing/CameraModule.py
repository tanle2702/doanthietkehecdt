import cv2

cap = cv2.VideoCapture(0)

def getImg(display=False):
    _, img = cap.read()
    if display:
        cv2.imshow('Camera', img)
    return img

if __name__ == '__main__':
    while True:
        img = getImage(display=True)
