from platform import release
import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

while(True):
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
cv2.imshow('frame')

k = cv2.waitKey(1)
if k%256 == 27:
    # ESC pressed
    print("Escape hit, closing...")

# elif k%256 ==32:
#     # SPACE pressed
#     img_name = "opencv_frame_{}.png".format(img_counter)

cam.release()
cv2.destroyAllWindows()