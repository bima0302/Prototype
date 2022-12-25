import numpy as np 
import cv2
import imutils

# from image
# img = cv2.imread('dataset/tipburn/tb_3.jpg', cv2.IMREAD_COLOR)
img = cv2.imread('dataset/normal/nm_16.jpg', cv2.IMREAD_COLOR)

# ================================================= #
## main code
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# range nilai hsv untuk masking
batas_bawah = (20, 100, 20)
batas_atas = (30, 180, 80)

# masking menggunkan thresholding
mask = cv2.inRange(imgHSV, batas_bawah, batas_atas)

# passing the bitwise_and over
# each pixel convoluted
res = cv2.bitwise_and(img, img, mask = mask)
    
# defining the kernel i.e. Structuring element
kernel = np.ones((5, 5), np.uint8)
    
# defining the closing function 
# over the image and structuring element
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
dilation = cv2.dilate(mask, kernel, iterations=1)

cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
for c in cnts:
    rect = cv2.boundingRect(c)
    # ukuran objek yang anggap tip burn
    if rect[2] < 10 or rect[3] < 10: continue
    x,y,w,h = rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
    cv2.putText(img,'Disease Detected',(x+w+10,y+h),0,0.5,(255,255,255),2)

# Display the resulting frame
cv2.imshow('img', img)
cv2.imshow("HSV mask", mask)
cv2.imshow("HSV closing filter", closing)

cv2.waitKey(0)
cv2.destroyAllWindows()