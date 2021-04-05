import cv2
import numpy as np

userClickPoint = []
def clickToAddPoint(event, x, y, flags, param):
    global userClickPoint
    
    if event == cv2.EVENT_LBUTTONDOWN:
        userClickPoint.append((x,y))
        cv2.circle(img, userClickPoint[-1], 10 , (0,0,255), -1)
        cv2.imshow('image', img)

    
def multipointTransform(original_img, userClickPoint,w,h):
    point1 = np.float32(userClickPoint)
    point2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(point1, point2)
    transformed = cv2.warpPerspective(original_img,matrix,(w,h))
    return transformed

def crop(img, point1, point2): #point1 = (x,y)
    return img[point1[1]:point2[1],point1[0]:point2[0]]

if __name__ == '__main__':
    img = cv2.imread('IMG_5467.JPG')
    copy = img.copy()
    h,w,c = img.shape
    cropped = crop(img, (30,40), (200,400))
    cv2.namedWindow('roi')
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', clickToAddPoint)
    while True:
        cv2.imshow('image', img)
        cv2.imshow('crop', cropped)
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'):
            break

        if key == ord('r'):
            userClickPoint = []
            img = copy.copy()

        if len(userClickPoint)==4:
            transformed = multipointTransform(copy, userClickPoint, w, h)
            cv2.imshow('roi', transformed)
