import numpy as np 
import cv2

cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
    # from image
    # img = cv2.imread('colors.jpg', cv2.IMREAD_COLOR)

    # ================================================= #
    ## main code
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    batas_bawah = (10, 0, 0)
    batas_atas = (30, 255, 100)
    mask = cv2.inRange(imgHSV, batas_bawah, batas_atas)

    # Display the resulting frame
    cv2.imshow('img', img)
    cv2.imshow("HSV mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()