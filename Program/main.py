# Abimanyu Sri Setyo
# 195150300111005

# Import Library
import cv2
import sys
import time
import imutils
import numpy as np
import argparse

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap 
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QWidget
from PyQt5.uic import loadUi
from collections import deque

# Import Date for Save Log
## Berfungsi untuk membuat penanggalan pada penamaan file saat menyimpan hasil deteksi
import time
date_string = time.strftime("%Y%m%d-%H%M")

# ===========================================================================================
# Main Code
## buffer sebagai prerender untuk mewakili warna 32 bit, 32 bit digunakan agar warna yang dihasilkan memiliki presisi yang cukup
### dalam beberapa percobaan, 24 bit tidak cukup dan 48 bit terlalu besar yang dapat berdampak pada waktu pemrosesannya
buffer = 32
# Set HSV value for object to be detected
## Berfungsi untuk membuat batas rentang HSV pada objek yang dideteksi
colorLower = (0, 0, 0)
colorUpper = (25, 255, 127)

pts = deque(maxlen=buffer)
counter = 0
(dX, dY) = (0, 0)
direction = ""
# berfungsi untuk menambah penundaan dalam eksekusi program. dipilih waktu 2 detik karena dirasa cukup
time.sleep(2.0)


class MainWindow(QDialog):
    # class constructor
    def __init__(self):
        # call QDialog constructor
        ## memuat file ui, file ini digunakan sebagai desain dari antarmuka aplikasi
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.logic = 0

        # create a timer
        ## membuat pengatur waktu, digunakan untuk menghitung apabila terdapat perubahan dalam rentang waktu tertentu
        ### perubahan ini dimaksudkan perubahan pada objek yang dideteksi secara realtime 
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # mendefinisikan runButton dengan parameter runButtonClicked yang berisi trigger klik
        self.runButton.clicked.connect(self.runButtonClicked)
        # mendefinisikan saveButton dengan parameter saveButtonClicked yang berisi trigger klik
        self.saveButton.clicked.connect(self.saveButtonClicked)
        # mendefinisikan quitButton dengan parameter quitButtonClicked yang berisi trigger klik
        self.quitButton.clicked.connect(self.quitButtonClicked)

    # membuat tombol run untuk menjalankan kamera
    def runButtonClicked(self):
        self.value = 1
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(1)
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
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        
        # create bounding box frame
        ## berfungsi untuk membuat kotak pada area daun yang terinfeksi penyakit
        for c in cnts:
            rect = cv2.boundingRect(c)
            # many box in same area
            if rect[2] < 10 or rect[3] < 10: continue
            x,y,w,h = rect
            # draw the rectangle on the frame
            # argument is cv2.rectangle(image,starting_point,ending_point,color,thickness)
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2)
            # put text on the rectangle frame
            # argument is cv2.putText(image,text,org,font,fontScale,color,thickness)    
            cv2.putText(image,'Disease Detected',(x+w+10,y+h),0,0.5,(255,255,255),2)    
        
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