import cv2
points = []
def clickToAddPoint(event, x, y, flags, param):
    global points
    
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))
        cv2.circle(img, points[-1], 10 , (0,0,255), -1)
        cv2.imshow('image', img)

    
def multipointTransform():
    pass

def crop(img, point1, point2): #point1 = (x,y)
    return img[point1[1]:point2[1],point1[0]:point2[0]]

if __name__ == '__main__':
    img = cv2.imread('color_conversion.jpg')
    cropped = crop(img, (30,40), (200,400))
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', clickToAddPoint)
    while True:
        cv2.imshow('image', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    # cv2.imshow('Orginal', img)
    # cv2.imshow('Cropped', cropped)
    # cv2.waitKey(0)
