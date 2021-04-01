import cv2
from utlis import stackImages

def cvtColor(img):
    color = cv2.imread(img)
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    return (color, gray) 

if __name__ == '__main__':
    color, gray = cvtColor('color_conversion.jpg')
    imgStacked = stackImages(0.5, ([color,gray]))
    cv2.imshow('Before and after', imgStacked)
    cv2.waitKey(0)
