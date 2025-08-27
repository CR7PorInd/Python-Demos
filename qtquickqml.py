import os

from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget


class QMLModule(QQuickWidget):
    def __init__(self, parent):
        super(QMLModule, self).__init__(parent=parent)
        os.environ['QT_QUICK_CONTROLS_STYLE'] = 'Universal'
        self.setSource(QUrl.fromLocalFile("demo.qml"))
        self.show()