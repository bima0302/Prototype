# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'theme/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)
        self.dashboardBox = QtWidgets.QGroupBox(Dialog)
        self.dashboardBox.setGeometry(QtCore.QRect(10, 10, 151, 481))
        self.dashboardBox.setObjectName("dashboardBox")
        self.cameraList = QtWidgets.QComboBox(self.dashboardBox)
        self.cameraList.setGeometry(QtCore.QRect(10, 20, 131, 24))
        self.cameraList.setObjectName("cameraList")
        self.cameraList.addItem("")
        self.cameraList.addItem("")
        self.selectCameraButton = QtWidgets.QPushButton(self.dashboardBox)
        self.selectCameraButton.setGeometry(QtCore.QRect(10, 50, 131, 24))
        self.selectCameraButton.setObjectName("selectCameraButton")
        self.runButton = QtWidgets.QPushButton(self.dashboardBox)
        self.runButton.setGeometry(QtCore.QRect(10, 80, 131, 24))
        self.runButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.runButton.setObjectName("runButton")
        self.saveButton = QtWidgets.QPushButton(self.dashboardBox)
        self.saveButton.setGeometry(QtCore.QRect(10, 420, 131, 24))
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveButton.setObjectName("saveButton")
        self.objectCoordinateText = QtWidgets.QTextBrowser(self.dashboardBox)
        self.objectCoordinateText.setGeometry(QtCore.QRect(10, 390, 131, 24))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.objectCoordinateText.setFont(font)
        self.objectCoordinateText.setObjectName("objectCoordinateText")
        self.objectCoordinateLabel = QtWidgets.QLabel(self.dashboardBox)
        self.objectCoordinateLabel.setGeometry(QtCore.QRect(10, 360, 131, 20))
        self.objectCoordinateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.objectCoordinateLabel.setObjectName("objectCoordinateLabel")
        self.runningText = QtWidgets.QTextBrowser(self.dashboardBox)
        self.runningText.setGeometry(QtCore.QRect(10, 110, 131, 24))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.runningText.setFont(font)
        self.runningText.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.runningText.setObjectName("runningText")
        self.saveText = QtWidgets.QTextBrowser(self.dashboardBox)
        self.saveText.setGeometry(QtCore.QRect(10, 450, 131, 24))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.saveText.setFont(font)
        self.saveText.setObjectName("saveText")
        self.objectPreviewBox = QtWidgets.QGroupBox(Dialog)
        self.objectPreviewBox.setGeometry(QtCore.QRect(169, 9, 521, 481))
        self.objectPreviewBox.setObjectName("objectPreviewBox")
        self.objectPreview = QtWidgets.QLabel(self.objectPreviewBox)
        self.objectPreview.setGeometry(QtCore.QRect(10, 20, 501, 451))
        self.objectPreview.setAutoFillBackground(False)
        self.objectPreview.setFrameShape(QtWidgets.QFrame.Box)
        self.objectPreview.setFrameShadow(QtWidgets.QFrame.Raised)
        self.objectPreview.setLineWidth(2)
        self.objectPreview.setScaledContents(True)
        self.objectPreview.setObjectName("objectPreview")
        self.objectPreviewBox.raise_()
        self.dashboardBox.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Aplikasi Deteksi Hama"))
        self.dashboardBox.setTitle(_translate("Dialog", "Dashboard"))
        self.cameraList.setItemText(0, _translate("Dialog", "Camera 1"))
        self.cameraList.setItemText(1, _translate("Dialog", "Camera 2"))
        self.selectCameraButton.setText(_translate("Dialog", "Select Camera"))
        self.runButton.setText(_translate("Dialog", "Run"))
        self.saveButton.setText(_translate("Dialog", "Save Log"))
        self.objectCoordinateLabel.setText(_translate("Dialog", "Object Coordinate"))
        self.objectPreviewBox.setTitle(_translate("Dialog", "Object Preview"))
        self.objectPreview.setText(_translate("Dialog", "Object Preview"))
