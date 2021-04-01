import cv2
import imutils

if __name__ == '__main__':
    image = cv2.imread('color_conversion.jpg')

    rotated_cv = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE) #rotation with cropping image
    rotated_imutils = imutils.rotate(image,45) #rotation with cropping image
    rotated_bound = imutils.rotate_bound(image,-45) # rotation without cropping image

    cv2.imshow('1', rotated_cv)
    cv2.imshow('2', rotated_imutils)
    cv2.imshow('3', rotated_bound)

    cv2.waitKey(0)
