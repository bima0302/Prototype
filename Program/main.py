# Abimanyu Sri Setyo
# 195150300111005

# Import Library
import cv2
import sys
import time
import imutils
import numpy as np
import argparse

from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap 
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QWidget
from PyQt5.uic import loadUi
from collections import deque

from PyQt5.QtCore import QTimer

# Import Date for Save Log
import time
date_string = time.strftime("%Y%m%d-%H%M")

# ===========================================================================================
# Main Code
buffer = 32
# Set HSV value for object to be detected
colorLower = (29, 86, 6)
colorUpper = (64, 255, 255)

pts = deque(maxlen=buffer)
counter = 0
(dX, dY) = (0, 0)
direction = ""

time.sleep(2.0)


class MainWindow(QDialog):
    # class constructor
    def __init__(self):
        # call QDialog constructor
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.logic = 0

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        
        self.runButton.clicked.connect(self.runButtonClicked)
        
        self.saveButton.clicked.connect(self.saveButtonClicked)

        self.quitButton.clicked.connect(self.quitButtonClicked)


    def runButtonClicked(self):
        self.value = 1
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start()
            # update control_bt text
            self.runButton.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.runButton.setText("Run")
        
    def saveButtonClicked(self):
        self.logic = 2
        
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()

        # convert image to RGB format
        image = imutils.resize(image, width=600)
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        
        # create bounding box frame
        for c in cnts:
            rect = cv2.boundingRect(c)
            if rect[2] < 100 or rect[3] < 100: continue
            print(cv2.contourArea(c))
            x,y,w,h = rect
            # draw the rectangle on the frame
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            # put text on the rectangle frame
            cv2.putText(image,'Disease Detected',(x+w+10,y+h),0,0.3,(0,255,0))    
        
        # convert image to RGB format 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.objectPreview.setPixmap(QPixmap.fromImage(qImg))
        
        # save log to .png file
        if(self.logic==2):   
            self.value = self.value + 1
            self.saveButton.setText("Saved!")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite('logs/image-' + date_string + '.png',image)
            self.logic=1       

    def quitButtonClicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())