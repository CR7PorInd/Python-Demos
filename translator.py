import asyncio

from googletrans import Translator
from googletrans.constants import LANGUAGES, LANGCODES

from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QPlainTextEdit, QPushButton


class TranslatorModule(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QFormLayout()
        self.setLayout(self.mainLayout)

        self.srcLang = "en"
        self.targetLang = "hi"

        self.srcLangBox = QComboBox()
        self.mainLayout.addRow("Source Language", self.srcLangBox)

        for item in list(LANGCODES.keys()):
            self.srcLangBox.addItem(item.capitalize())

        self.srcLangBox.currentTextChanged.connect(self.changeSourceLanguage)

        self.targetLangBox = QComboBox()
        self.mainLayout.addRow("Target Language", self.targetLangBox)

        for item in list(LANGCODES.keys()):
            self.targetLangBox.addItem(item.capitalize())

        self.targetLangBox.currentTextChanged.connect(self.changeTargetLanguage)

        self.inputText = QPlainTextEdit()
        self.mainLayout.addWidget(self.inputText)

        self.srcLangBox.setCurrentText(LANGUAGES[self.srcLang].capitalize())
        self.targetLangBox.setCurrentText(LANGUAGES[self.targetLang].capitalize())

        self.translateBtn = QPushButton("Translate")
        self.mainLayout.addRow(f"Click this button to translate.", self.translateBtn)
        self.translateBtn.clicked.connect(lambda: asyncio.run(self.translateText()))

        self.outputText = QPlainTextEdit()
        self.outputText.setReadOnly(True)
        self.mainLayout.addWidget(self.outputText)

    def changeSourceLanguage(self):
        print(self.srcLang, self.targetLang, self.srcLangBox.currentText())
        if LANGCODES[self.srcLangBox.currentText().lower()] == self.targetLang:
            self.srcLang, self.targetLang = self.targetLang, self.srcLang
        else:
            self.srcLang = LANGCODES[self.srcLangBox.currentText().lower()]
        self.targetLangBox.setCurrentText(LANGUAGES[self.targetLang].capitalize())
        self.srcLangBox.setCurrentText(LANGUAGES[self.srcLang].capitalize())



    def changeTargetLanguage(self):
        print(self.srcLang, self.targetLang, self.targetLangBox.currentText())
        if LANGCODES[self.targetLangBox.currentText().lower()] == self.srcLang:
            self.targetLang, self.srcLang = self.srcLang, self.targetLang
        else:
            self.targetLang = LANGCODES[self.targetLangBox.currentText().lower()]
        self.targetLangBox.setCurrentText(LANGUAGES[self.targetLang].capitalize())
        self.srcLangBox.setCurrentText(LANGUAGES[self.srcLang].capitalize())

    async def translateText(self):
        async with Translator() as translator:
            translatedText = await translator.translate(self.inputText.toPlainText(), self.targetLang)
            print(translatedText.text)
            self.outputText.setPlainText(translatedText.text)

