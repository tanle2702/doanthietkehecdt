from skimage.metrics import structural_similarity
import imutils
import cv2

imageA = cv2.imread('imageA.jpg')
imageB = cv2.imread('imageB.jpg')

grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

(score, diff) =  structural_similarity(grayA, grayB, full=True)
diff = (diff*255).astype('uint8')
print('SSIM: ', (score+1)*127) #lower number means img more different


thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    cv2.rectangle(imageA, (x,y), (x+w, y+h), (0,255,0),10)
    cv2.rectangle(imageB, (x,y), (x+w, y+h), (0,0,255),10)

cv2.imshow('Original', imageA)
cv2.imshow('Modified', imageB)
cv2.waitKey(0)

