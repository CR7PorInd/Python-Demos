from threading import Thread

import google.genai as gemini
import speech_recognition as sr
from PIL.Image import Image
from PIL.Image import open as ImageOpen
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget, QListWidget, QLineEdit, QHBoxLayout, QLabel, QPushButton, QTextEdit, \
    QListWidgetItem, QAbstractItemView, QScrollArea, QFileDialog, QApplication

API_KEY = "AIzaSyBbU2UjqR6etgMxCGS3OTcwOttt8qy9vOs"


class GeminiModule(QWidget):
    def __init__(self):
        super().__init__()

        # Persistent chat session
        self.client = gemini.Client(api_key=API_KEY)

        self.chat = self.client.chats.create(model="gemini-2.0-flash")

        self.recognizer = sr.Recognizer()

        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        self.chatList = QListWidget(self)
        self.chatList.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.chatList.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.mainLayout.addWidget(self.chatList)

        self.inputRow = QHBoxLayout(self)
        self.mainLayout.addLayout(self.inputRow)

        self.imageUpload = QPushButton("Upload", self)
        self.imageUpload.clicked.connect(self.onImageSent)
        self.inputRow.addWidget(self.imageUpload)

        self.inputTextEdit = QLineEdit(self)
        self.inputTextEdit.returnPressed.connect(self.onMessageSent)
        self.inputRow.addWidget(self.inputTextEdit)

        self.voiceInput = QPushButton("Speak", self)
        self.voiceInput.clicked.connect(self.onVoiceInput)
        self.inputRow.addWidget(self.voiceInput)

        self.sendButton = QPushButton("Send", self)
        self.sendButton.clicked.connect(self.onMessageSent)
        self.inputRow.addWidget(self.sendButton)


        self.chatWidgets = []

    def sendMessage(self):
        text = self.chat.send_message(self.inputTextEdit.text().strip()).text
        self.updateList(text, "text")

    def sendPic(self, image2: Image):
        print(type(image2))
        text = self.chat.send_message(image2).text
        self.updateList(text, "image", image=image2)

    def getVoiceCommand(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=10)
                command: str = self.recognizer.recognize_google(audio)
                self.voiceInput.setText("Speak")
                QApplication.processEvents()
                if command.strip() == "":
                    self.enableButtons()
                    self.inputTextEdit.clear()
                    QApplication.processEvents()
                    return
                response = self.chat.send_message(command.strip()).text
                self.updateList(response, "text", user_input=command)
            except Exception:
                self.voiceInput.setText("Speak")
                self.inputTextEdit.clear()
                self.enableButtons()
                QApplication.processEvents()

    def onVoiceInput(self):
        self.voiceInput.setText("Listening...")
        self.disableButtons()
        QApplication.processEvents()

        worker = Thread(target=self.getVoiceCommand, daemon=True)
        worker.run()

    def disableButtons(self):
        self.sendButton.setEnabled(False)
        self.voiceInput.setEnabled(False)
        self.imageUpload.setEnabled(False)

    def enableButtons(self):
        self.sendButton.setEnabled(True)
        self.voiceInput.setEnabled(True)
        self.imageUpload.setEnabled(True)


    def onMessageSent(self):
        if self.inputTextEdit.text().strip() == "":
            return


        QApplication.processEvents()

        worker = Thread(target=self.sendMessage, daemon=True)
        worker.run()

    def onImageSent(self):

        image, _ = QFileDialog.getOpenFileName(self, "Select Image", "Upload Image",
                                               "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if image:
            self.disableButtons()
            QApplication.processEvents()

            worker = Thread(target=self.sendPic, args=(ImageOpen(image),), daemon=True)
            worker.run()

    def updateList(
        self,
        respondedText: str,
        datatype: str = "text",
        user_input: str = None,
        image: Image = None
    ):
        userInput = self.inputTextEdit.text().strip() if user_input is None else user_input
        print(respondedText)
        response = QLabel(respondedText + "\n\n")
        response.setFixedWidth(800)
        response.setMinimumHeight(60)
        response.setWordWrap(True)
        response.setTextFormat(Qt.TextFormat.MarkdownText)

        scrollArea = QScrollArea()
        scrollArea.setWidget(response)
        scrollArea.setWidgetResizable(True)
        scrollArea.setMinimumHeight(100)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(scrollArea)
        layout.setContentsMargins(0, 0, 0, 0)

        if datatype == "image" and image is not None:
            label1 = QLabel()
            label1.setPixmap(QPixmap(image.toqpixmap()))
            label1.setFixedSize(image.width, image.height)
            label1.setAlignment(Qt.AlignmentFlag.AlignRight)
            item1 = QListWidgetItem()
            item1.setSelected(False)
            item1.setSizeHint(label1.sizeHint())
            item1.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.chatList.addItem(item1)
            self.chatList.setItemWidget(item1, label1)
        else:
            item1 = QListWidgetItem(userInput)
            item1.setSelected(False)
            item1.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.chatList.addItem(item1)

        item = QListWidgetItem()
        item.setSelected(False)
        item.setSizeHint(container.sizeHint())
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)

        self.chatList.addItem(item)
        self.chatList.setItemWidget(item, container)

        self.inputTextEdit.clear()
        self.voiceInput.setText("Speak")
        self.enableButtons()

        QApplication.processEvents()
