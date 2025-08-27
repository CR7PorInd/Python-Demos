from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

import sys

from mainwindow import MainWindow

app = QApplication(sys.argv)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)
# apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)

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
app.setStyle("Fusion")

window = MainWindow()
window.showMaximized()

sys.exit(app.exec())