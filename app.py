from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

import sys

from mainwindow import MainWindow

app = QApplication(sys.argv)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)

fid = QFontDatabase.addApplicationFont("Roboto.ttf")
if fid == -1:
    print("UNABLE TO LOAD FONT!")
else:
    app.setFont(QFont('Roboto'))

with open('material3.css', 'r') as stylesheet:
    app.setStyleSheet(stylesheet.read())

app.setApplicationName("Python Demos App")
app.setApplicationVersion("1.0.0")
app.setQuitOnLastWindowClosed(True)
app.setApplicationDisplayName("Python Demos App")
app.setStyle("Fusion")

window = MainWindow()
window.showMaximized()

sys.exit(app.exec())