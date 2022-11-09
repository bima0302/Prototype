# Abimanyu Sri Setyo
# 195150300111005

# Import Library
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

# Import Theme
from theme import main

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


class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = main.Ui_Dialog()
        self.ui.setupUi(self)

        # set online webcam list for choose camera
        #### BELOM JADIII ####
        # self.onlineCameraList = QCameraInfo.availableCameras()
        # self.cameraList.addItems([c.description() for c in self.onlineCameraList])
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        
        self.ui.runButton.clicked.connect(self.runButtonClicked)
        
        self.logic = 0
        self.value = 1
        self.ui.saveButton.clicked.connect(self.saveButtonClicked)
    
    def saveButtonClicked(self):
        self.logic =2
        
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
        
        
        # only proceed if at least one contour was found
        for c in cnts:
            rect = cv2.boundingRect(c)
            if rect[2] < 100 or rect[3] < 100: continue
            print(cv2.contourArea(c))
            x,y,w,h = rect
            # draw the rectangle and centroid on the frame,
            # then update the list of tracked points
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
        self.ui.objectPreview.setPixmap(QPixmap.fromImage(qImg))
        
        if(self.logic==2):   
            self.value = self.value + 1
            self.ui.saveButton.setText("Saved!")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite('logs/image-' + date_string + '.png',image)
            self.logic=1       
    
    def runButtonClicked(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start()
            # update control_bt text
            self.ui.runButton.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.runButton.setText("Run")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())