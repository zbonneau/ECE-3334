import cv2
import numpy as np

camera: cv2.VideoCapture = cv2.VideoCapture(1)

if (not camera.isOpened()):
    exit()

BLURSIZE = 5
THRESHOLD_OFFSET = 50
FONT = cv2.FONT_HERSHEY_PLAIN

CARD_SIZE_MAX = 30000
CARD_SIZE_MIN = 25000
while 1:
    _, frame = camera.read()
    

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("GrayScale", grayscale)

    blur = cv2.GaussianBlur(grayscale, (BLURSIZE, BLURSIZE), 0)

    cv2.imshow("Contrast", blur)

    img_w, img_h = np.shape(blur)[:2]
    bkg_level = grayscale[int(img_h/100)][int(img_w/2)]
    threshold = bkg_level + THRESHOLD_OFFSET
    _, threshed = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

    cv2.imshow("Threshold", threshed)

    contours, heirarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) == 0): 
        continue

    isCard = np.zeros(len(contours), dtype=int)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        perimeter = cv2.arcLength(contour,True)
        approx_corners = cv2.approxPolyDP(contour,0.01*perimeter, True)

        if ((area < CARD_SIZE_MAX) and (area > CARD_SIZE_MIN)
            and (len(approx_corners) == 4)):
            isCard[pic] = 1
            cv2.circle(frame, ((int)(x+w/2), (int(y+h/2))), 5 ,(255,0,0), -1)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 1)
            cv2.putText(frame, "area: "+str(area), (x,y+h), FONT, 1.5, (255,255,255), thickness=4)
        
    cv2.imshow("frame", frame)

    char = (cv2.waitKey(1) & 0xff)
    if (char == ord('q')): 
        break

    elif (char == ord('p')):
        print(isCard)
        cv2.waitKey(0)


cv2.destroyAllWindows()
camera.release()