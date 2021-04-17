import cv2
import imutils
def detectShape(contour):
    shape = 'unknown'
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04*peri, True)

    if len(approx) == 3:
        shape = 'triangle'

    elif len(approx) == 4:
        (x,y,w,h) = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = 'square' if ar >= 0.95 and ar <= 1.05 else 'rectangle'

    elif len(approx) == 5:
        shape = 'pentagon'

    else:
        shape = 'circle'

    return shape

if __name__ == '__main__':
    image = cv2.imread('contours.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 60,255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        M = cv2.moments(contour)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = detectShape(contour)
        cv2.drawContours(image, [contour], -1, (0,255,0),10)
        cv2.putText(image, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2 )

        cv2.imshow('image', image)
        cv2.waitKey(0)


