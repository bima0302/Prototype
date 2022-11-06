# Abimanyu Sri Setyo
# 195150300111005

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QDialog
from PyQt5 import uic
import sys
import cv2

from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time

buffer = 32

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

pts = deque(maxlen=buffer)
counter = 0
(dX, dY) = (0, 0)
direction = ""

time.sleep(2.0)

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = uic.loadUi("main.ui",self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        
        self.ui.pushButton_2.clicked.connect(self.controlTimer)
        
        self.logic = 0
        self.value = 1
        self.ui.pushButton_3.clicked.connect(self.CaptureClicked)
    
    def CaptureClicked(self):
        self.logic =2
        
    def viewCam(self):
        # self.cap = cv2.VideoCapture(0)
        # start timer
        # self.timer.start(20)
        # read image in BGR format
        ret, image = self.cap.read()
        
        # convert image to RGB format
        image = imutils.resize(image, width=600)
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea) 
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(image, center, 5, (0, 0, 255), -1)
               
                # to show object cooordinate
                x_coordinate = center[0]
                y_coordinate = center[1]
                text = f'x: {x_coordinate},  y: {y_coordinate}'
                if x is not None and y is not None:
                    self.ui.TEXT_2.setText(text)
                # to show object cooordinate
        
        
        
            # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # check to see if enough points have been accumulated in
            # the buffer
            if counter >= 10 and i == 1 and pts[-10] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
                (dirX, dirY) = ("", "")

                # ensure there is significant movement in the
                # x-direction
                if np.abs(dX) > 20:
                    dirX = "East" if np.sign(dX) == 1 else "West"

                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > 20:
                    dirY = "North" if np.sign(dY) == 1 else "South"

                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    direction = "{}-{}".format(dirY, dirX)

                # otherwise, only one direction is non-empty
                else:
                    direction = dirX if dirX != "" else dirY

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(buffer/ float(i + 1)) * 2.5)
            cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)
        
        # convert image to RGB format 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.imgLabel_1.setPixmap(QPixmap.fromImage(qImg))
        
        # get image blurred
        height_2, width_2, channel_2 = blurred.shape
        step_2 = channel_2 * width_2
        qImg_2 =  QImage(blurred.data, width_2, height_2, step_2, QImage.Format_RGB888)
        # self.ui.imgLabel_2.setPixmap(QPixmap.fromImage(qImg_2))
        
        # get image hsv
        height_3, width_3, channel_3 = hsv.shape
        step_3 = channel_3 * width_3
        qImg_3 =  QImage(hsv.data, width_3, height_3, step_3, QImage.Format_RGB888)
        # self.ui.imgLabel_3.setPixmap(QPixmap.fromImage(qImg_3))
        
        # get image mask
        height_4, width_4= mask.shape
        step_4 = 3 * width_4 
        qImg_4 =  QImage(mask.data, width_4, height_4, QImage.Format_Grayscale8)
        # self.ui.imgLabel_4.setPixmap(QPixmap.fromImage(qImg_4))
    
        if(self.logic==2):   
            self.value = self.value + 1
            self.ui.TEXT_3.setText("Saved!")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite('capture.png',image)
            self.logic=1       
    
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.TEXT_4.setText("Running")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.TEXT_4.setText("Stop")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())