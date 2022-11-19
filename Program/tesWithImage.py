import numpy as np 
import cv2

# from image
img = cv2.imread('image1.jpg', cv2.IMREAD_COLOR)

# ================================================= #
## main code
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

batas_bawah = (10, 0, 0)
batas_atas = (30, 255, 100)
mask = cv2.inRange(imgHSV, batas_bawah, batas_atas)

# Display the resulting frame
cv2.imshow('img', img)
cv2.imshow("HSV mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()