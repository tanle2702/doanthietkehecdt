import argparse
import cv2

refPt = []
cropping = False

def clickAndCrop(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x,y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x,y))
        cropping = False

        cv2.rectangle(image, refPt[0], refPt[1], (0,255,0), 2)
        cv2.imshow('image', image)

if __name__ == '__main__':
    image = cv2.imread('color_conversion.jpg')
    clone = image.copy()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', clickAndCrop)
    while True:
        cv2.imshow('image', image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            image = clone.copy()

        if key == ord('c'):
            break

    if len(refPt)== 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow('roi',roi)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
