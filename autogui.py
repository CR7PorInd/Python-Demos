from typing import List, Tuple

import pyautogui
from PySide6.QtWidgets import QTabWidget, QTextEdit, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from threading import Thread

class HotKeyDemo(QWidget):
    def __init__(self):
        super(HotKeyDemo, self).__init__()
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(10)

        # ===== Row 1 =====
        self.row1 = QHBoxLayout()
        self.label1 = QLabel("Open Automatic Typing (Shift+Alt+T)")
        self.button1 = QPushButton("ACTIVATE")
        self.button1.clicked.connect(lambda: self.activateHotkey(["shift", "alt", "t"]))
        self.button1.setFixedWidth(100)
        self.row1.addWidget(self.label1)
        self.row1.addStretch()
        self.row1.addWidget(self.button1)
        self.mainLayout.addLayout(self.row1)

        # ===== Row 2 =====
        self.row2 = QHBoxLayout()
        self.label2 = QLabel("Open Task Manager (Ctrl+Shift+Escape)")
        self.button2 = QPushButton("ACTIVATE")
        self.button2.clicked.connect(lambda: self.activateHotkey(["ctrl", "shift", "escape"]))
        self.button2.setFixedWidth(100)
        self.row2.addWidget(self.label2)
        self.row2.addStretch()
        self.row2.addWidget(self.button2)
        self.mainLayout.addLayout(self.row2)

        # ===== Row 3 =====
        self.row3 = QHBoxLayout()
        self.label3 = QLabel("Open System Settings (Windows+I)")
        self.button3 = QPushButton("ACTIVATE")
        self.button3.clicked.connect(lambda: self.activateHotkey(["win", "i"]))
        self.button3.setFixedWidth(100)
        self.row3.addWidget(self.label3)
        self.row3.addStretch()
        self.row3.addWidget(self.button3)
        self.mainLayout.addLayout(self.row3)

        # ===== Row 4 =====
        self.row4 = QHBoxLayout()
        self.label4 = QLabel("Open Run Dialog (Windows+R)")
        self.button4 = QPushButton("ACTIVATE")
        self.button4.clicked.connect(lambda: self.activateHotkey(["win", "r"]))
        self.button4.setFixedWidth(100)
        self.row4.addWidget(self.label4)
        self.row4.addStretch()
        self.row4.addWidget(self.button4)
        self.mainLayout.addLayout(self.row4)

        # ===== Row 5 =====
        self.row5 = QHBoxLayout()
        self.label5 = QLabel("Open Windows Explorer (Windows+E)")
        self.button5 = QPushButton("ACTIVATE")
        self.button5.clicked.connect(lambda: self.activateHotkey(["win", "e"]))
        self.button5.setFixedWidth(100)
        self.row5.addWidget(self.label5)
        self.row5.addStretch()
        self.row5.addWidget(self.button5)
        self.mainLayout.addLayout(self.row5)

        # ===== Row 6 =====
        self.row6 = QHBoxLayout()
        self.label6 = QLabel("Snipping Tool (Windows+Shift+S)")
        self.button6 = QPushButton("ACTIVATE")
        self.button6.clicked.connect(lambda: self.activateHotkey(["win", "shift", "s"]))
        self.button6.setFixedWidth(100)
        self.row6.addWidget(self.label6)
        self.row6.addStretch()
        self.row6.addWidget(self.button6)
        self.mainLayout.addLayout(self.row6)

        # ===== Row 7 =====
        self.row7 = QHBoxLayout()
        self.label7 = QLabel("New Desktop (Windows+Ctrl+D)")
        self.button7 = QPushButton("ACTIVATE")
        self.button7.clicked.connect(lambda: self.activateHotkey(["win", "ctrl", "d"]))
        self.button7.setFixedWidth(100)
        self.row7.addWidget(self.label7)
        self.row7.addStretch()
        self.row7.addWidget(self.button7)
        self.mainLayout.addLayout(self.row7)

    def activateHotkey(self, keys: List[str]):
        hotkeyThread = Thread(target=self.hotkeyThreaded, args=(keys,), daemon=True)
        hotkeyThread.start()

    def hotkeyThreaded(self, keys: List[str]):
        pyautogui.hotkey(*keys)

class PyAutoGUIModule(QTabWidget):
    def __init__(self):
        super().__init__()

        self.autoType = QTextEdit()
        self.addTab(self.autoType, "Automatic Typing")

        self.hotkeyDemo = HotKeyDemo()
        self.addTab(self.hotkeyDemo, "Automatic Key Press")

        self.typingCount = 0

    def startTyping(self):
        self.typingCount += 1

        self.setCurrentIndex(0)
        self.autoType.setFocus()

        typingThread = Thread(target=self.typingThreaded, daemon=True)
        typingThread.start()

    def typingThreaded(self):
        pyautogui.typewrite(
            message=f"Typing Demo No. {self.typingCount}: This is a random sentence.",
            interval=0.05
        )
