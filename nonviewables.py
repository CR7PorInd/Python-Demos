import subprocess
import sys
from threading import Thread

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QApplication


class NonViewableDemosModule(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(10)

        # ===== Row 1 =====
        self.row1 = QHBoxLayout()
        self.label1 = QLabel("Typing Hack - Selenium Web Driver")
        self.button1 = QPushButton("RUN")
        self.button1.clicked.connect(self.runTypingHack)
        self.button1.setFixedWidth(100)
        self.row1.addWidget(self.label1)
        self.row1.addStretch()
        self.row1.addWidget(self.button1)
        self.mainLayout.addLayout(self.row1)

    def subprocessRunner(self):
        subprocess.run('\"{0}\" typingcheater.py'.format(sys.executable.replace("\\", "/")))
        self.button1.setEnabled(True)
        QApplication.processEvents()

    def runTypingHack(self):
        self.button1.setEnabled(False)
        QApplication.processEvents()
        thread = Thread(target=self.subprocessRunner, daemon=True)
        thread.start()
