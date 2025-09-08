from typing import Union

import PIL.Image
from PIL import ImageQt
from PIL import Image
from PySide6.QtGui import QAction, QPixmap, Qt, QIcon

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QToolBar, QFileDialog, QStyleFactory, QStyle, QMessageBox, \
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


class ImageEditorModule(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)

        self.image: Union[Image.Image | None] = None
        self.imagePrevious: Union[Image.Image | None] = None
        self.imagePath: str = None

        self.toolbar = QToolBar(self)
        self.mainLayout.setMenuBar(self.toolbar)

        self.scene = QGraphicsScene()

        self.imageDisplay = QGraphicsView(self.scene)
        self.mainLayout.addWidget(self.imageDisplay)
        self.imageDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageDisplay.setFixedSize(800, 650)

        self.openAction = QAction("Open", self)
        self.openAction.triggered.connect(self.openImage)
        self.openAction.setStatusTip("Open an image file.")
        self.openAction.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        self.openAction.setShortcut("Ctrl+Shift+I")
        self.toolbar.addAction(self.openAction)

        self.saveAction = QAction("Save", self)
        self.saveAction.triggered.connect(self.saveImage)
        self.saveAction.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.saveAction.setShortcut("Alt+Ctrl+S")
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.rotateClockAction = QAction("Rotate Clockwise", self)
        self.rotateClockAction.triggered.connect(lambda: self.rotateImage(270))
        self.rotateClockAction.setIcon(QIcon('clock.png'))
        self.rotateClockAction.setShortcut('Shift+Alt+C')
        self.toolbar.addAction(self.rotateClockAction)

        self.rotateAntiClockAction = QAction("Rotate Anticlockwise", self)
        self.rotateAntiClockAction.triggered.connect(lambda: self.rotateImage(90))
        self.rotateAntiClockAction.setIcon(QIcon('anticlock.png'))
        self.rotateAntiClockAction.setShortcut('Shift+Alt+A')
        self.toolbar.addAction(self.rotateAntiClockAction)

        self.saveAction.setEnabled(False)
        self.rotateClockAction.setEnabled(False)
        self.rotateAntiClockAction.setEnabled(False)

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", filter="Image Files (*.png *.jpg *.jpeg *.bmp)")
        if imagePath:
            self.imagePath = imagePath
            self.image = Image.open(imagePath)
            self.saveAction.setEnabled(True)
            self.rotateClockAction.setEnabled(True)
            self.rotateAntiClockAction.setEnabled(True)
            self.updateImage()

    def rotateImage(self, angle: int = 360):
        self.imagePrevious = self.image
        self.image = self.image.rotate(angle)
        self.updateImage()

    def updateImage(self):
        self.scene.clear()
        self.image.thumbnail((800, 650), Image.Resampling.LANCZOS)
        self.scene.addItem(QGraphicsPixmapItem(self.image.toqpixmap()))

    def saveImage(self):
        self.image.save(self.imagePath)
        QMessageBox.information(self, "Saved", "Image has been saved.")

