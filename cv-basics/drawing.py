import cv2
import numpy as np

if __name__ == '__main__':
    blank_image = np.ones((600,1200,3)) * 255 #create a blank image

    #Create text
    text = 'Hello world!!'
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text,font,1,2)[0] # getTextSize return ((length,height),10)
    #calc center of the text
    textX = blank_image.shape[1]//2 - text_size[0]//2
    textY = blank_image.shape[0]//2 - text_size[1]//2
    cv2.putText(blank_image, 
            text, 
            (textX,textY), #(x,y)
            fontFace=font, 
            fontScale=1, 
            color=(0,0,0))

    #Draw line
    cv2.line(blank_image, (0,0), (blank_image.shape[1],blank_image.shape[0]), color=(0,255,0), thickness=5)
    #Draw circle
    cv2.circle(blank_image, (textX,textY), radius=25, color=(255,0,255), thickness=2 )

    #Draw polygons

    cv2.rectangle(blank_image, (20,40), (60,80),color=(255,0,128), thickness=2)

    points = np.array([[0,0],[100,250],[300,30],[60,600]],np.int32)
    cv2.polylines(blank_image, [points], True, (0,255,255), thickness=3) #True to make closed polylines, False to make open polylines

    cv2.imshow('Drawing', blank_image)
    cv2.waitKey(0)
