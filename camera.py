import os

from PySide6.QtCore import QTimer
from PySide6.QtGui import QScreen
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMainWindow, QApplication
from PySide6.QtMultimedia import QImageCapture, QCamera, QMediaDevices, QMediaCaptureSession, QScreenCapture
from PySide6.QtWidgets import QWidget


class CameraModule(QWidget):
    def __init__(self, mainwindow: QMainWindow):
        super(CameraModule, self).__init__()

        self.mWindow = mainwindow

        self.widgetLayout = QVBoxLayout()
        self.setLayout(self.widgetLayout)

        self.videoWidget = QVideoWidget()
        self.widgetLayout.addWidget(self.videoWidget)

        self.camera = QCamera(QMediaDevices.defaultVideoInput())

        self.session = QMediaCaptureSession()
        self.session.setCamera(self.camera)
        self.session.setVideoOutput(self.videoWidget)

        self.capture = QImageCapture()
        self.capture.setQuality(QImageCapture.Quality.VeryHighQuality)
        self.capture.setFileFormat(QImageCapture.FileFormat.PNG)
        self.session.setImageCapture(self.capture)

        self.buttonLayout = QHBoxLayout()
        self.widgetLayout.addLayout(self.buttonLayout)

        self.captureButton = QPushButton("Take Photo", self)
        self.captureButton.clicked.connect(self.takePhoto)
        self.buttonLayout.addWidget(self.captureButton)

        self.ssButton = QPushButton("Take Screenshot (Window)", self)
        self.ssButton.clicked.connect(self.takeScreenshot)
        self.buttonLayout.addWidget(self.ssButton)

        self.camera.start()

    def takePhoto(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Photo", os.path.expanduser("~"), filter = "PNG (*.png)")
        if filePath:
            self.capture.captureToFile(filePath)

    def takeScreenshot(self):
        self.mWindow.showMinimized()

        filePath, _ = QFileDialog.getSaveFileName(self, "Save Photo", os.path.expanduser("~"), filter="PNG (*.png)")
        if filePath:
            screen = QApplication.primaryScreen()
            if screen is None:
                return

            def doAction():
                screenshot = screen.grabWindow(0)
                screenshot.save(filePath, "png")
                self.mWindow.showMaximized()

            QTimer.singleShot(1000, doAction)


