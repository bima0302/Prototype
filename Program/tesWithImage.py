import numpy as np 
import cv2
import imutils

# from image
img = cv2.imread('dataset/tipburn/pengujian/tb_1.jpg', cv2.IMREAD_COLOR)
# img = cv2.imread('dataset/normal/pengujian/nm_15.jpg', cv2.IMREAD_COLOR)
# 4,7,9,11
# ================================================= #
## main code
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

batas_bawah = (0, 80, 30)
batas_atas = (100, 180, 100)
mask = cv2.inRange(imgHSV, batas_bawah, batas_atas)

cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
for c in cnts:
    rect = cv2.boundingRect(c)
    # ukuran objek yang anggap tip burn
    if rect[2] < 8 or rect[3] < 8: continue
    x,y,w,h = rect
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
    cv2.putText(img,'Disease Detected',(x+w+10,y+h),0,0.5,(255,255,255),2)

# Display the resulting frame
cv2.imshow('img', img)
cv2.imshow("HSV mask", mask)

# save
cv2.imwrite('dataset/perancangan/bug2/tb.jpg', img)
cv2.imwrite('dataset/perancangan/bug2/tb_mask.jpg', mask)


cv2.waitKey(0)
cv2.destroyAllWindows()