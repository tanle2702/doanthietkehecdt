import cv2
from utlis import stackImages
import os

def showShape(img):
    height, width, channel = img.shape
    print('Width: ', width)
    print('Height: ', height)
    print('Channel: ', channel)

def resizeImage(img, width): #supply width as an arg, calc height to keep image ratio
    hO, wO, cO = img.shape
    ratio = wO/hO
    height = width/ratio
    return cv2.resize(img, (int(width),int(height)))

if __name__ == '__main__':
    display_size = True
    image = cv2.imread('color_conversion.jpg')
    cv2.imshow('Before', image)
    if display_size:
        print('Before resizing: ' + str(os.path.getsize('color_conversion.jpg')))
    resized = resizeImage(image, 300)
    cv2.imwrite('resized.jpg', resized)
    if display_size:
        print('After resizing: ' + str(os.path.getsize('resized.jpg')))
    showShape(resized)
    cv2.imshow('After', resized)
    cv2.waitKey(0)
