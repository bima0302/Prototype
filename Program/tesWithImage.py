import numpy as np 
import cv2
import imutils

# from image
img = cv2.imread('SL6.jpg', cv2.IMREAD_COLOR)

# ================================================= #
## main code
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

batas_bawah = (0, 0, 0)
batas_atas = (30, 255, 100)
mask = cv2.inRange(imgHSV, batas_bawah, batas_atas)

cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
for c in cnts:
    rect = cv2.boundingRect(c)
    # ukuran objek yang anggap tip burn
    if rect[2] < 60 or rect[3] < 60: continue
    x,y,w,h = rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2) 
    cv2.putText(img,'Disease Detected',(x+w+10,y+h),0,0.5,(255,255,255),2)

# Display the resulting frame
cv2.imshow('img', img)
cv2.imshow("HSV mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()