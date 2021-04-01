import cv2
from utlis import stackImages

if __name__ == '__main__':
    image = cv2.imread('color_conversion.jpg')
    canny = cv2.Canny(image, 100,200)
    
    stacked_canny = stackImages(0.5,[image,canny])
    cv2.imshow('Canny edge detection', stacked_canny)
    cv2.waitKey(0)

