from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QTableWidget,
                               QTableWidgetItem, QLabel, QHeaderView, QProgressBar)

from nltk import word_tokenize, pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Helpers:

    @staticmethod
    def getWordnetPos(treebankTag):
        if treebankTag.startswith('J'):
            return wordnet.ADJ
        elif treebankTag.startswith('V'):
            return wordnet.VERB
        elif treebankTag.startswith('N'):
            return wordnet.NOUN
        elif treebankTag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    @staticmethod
    def detectVerbFeatures(tag):
        tense = ""
        verbType = ""

        if tag == "VBD":
            tense = "Past"
        elif tag == "VBZ":
            tense = "Present"
        elif tag == "VBP":
            tense = "Present"
        elif tag == "VB":
            tense = "Base"
            verbType = "Infinitive/Base"
        elif tag == "VBG":
            verbType = "Gerund/Present participle"
            tense = "Continuous"
        elif tag == "VBN":
            verbType = "Past participle"
            tense = "Perfect/Past"

        return tense, verbType

    @staticmethod
    def detectNumber(tag, word):
        if tag in ["NNS", "NNPS"]:
            return "Plural"
        elif tag in ["NN", "NNP"]:
            return "Singular"
        elif tag in ["PRP"]:
            if word.lower() in ["they", "we", "you"]:
                return "Plural"
            elif word.lower() in ["he", "she", "it", "i"]:
                return "Singular"
        return ""

    @staticmethod
    def readablePos(tag):
        if tag.startswith("VB"):
            return "Verb"
        elif tag.startswith("NN"):
            return "Noun"
        elif tag.startswith("JJ"):
            return "Adjective"
        elif tag.startswith("RB"):
            return "Adverb"
        elif tag == "IN":
            return "Preposition"
        elif tag == "TO":
            return "Infinitive Marker"
        elif tag == ".":
            return "Punctuation"
        elif tag in [",", ":", "(", ")", "``", "''"]:
            return "Punctuation"
        elif tag.startswith("PRP"):
            return "Pronoun"
        elif tag.startswith("DT"):
            return "Determiner"
        elif tag == "CC":
            return "Conjunction"
        else:
            return "Other"

    @staticmethod
    def detectGender(word, tag):
        wordLower = word.lower()

        malePronouns = {"he", "him", "his", "brother", "father", "uncle", "grandfather", "nephew"}
        femalePronouns = {"she", "her", "hers", "sister", "mother", "aunt", "grandmother", "niece"}
        neutralPronouns = {"it", "its", "they", "them", "their", "i", "you", "we", "us"}

        if tag.startswith("PRP"):
            if wordLower in malePronouns:
                return "Male"
            elif wordLower in femalePronouns:
                return "Female"
            elif wordLower in neutralPronouns:
                return "Neutral"
        return ""  # Default if undetectable

    @staticmethod
    def analyzeSentence(sentence):
        tokens = word_tokenize(sentence)
        posTags = pos_tag(tokens)
        lemmatizer = WordNetLemmatizer()
        result = []

        for word, tag in posTags:
            wnTag = Helpers.getWordnetPos(tag)
            lemma = lemmatizer.lemmatize(word, wnTag)

            partOfSpeech = Helpers.readablePos(tag)
            tense, verbType = Helpers.detectVerbFeatures(tag)
            number = Helpers.detectNumber(tag, word)
            gender = Helpers.detectGender(word, tag)

            result.append({
                "word": word,
                "lemma": lemma,
                "partOfSpeech": partOfSpeech,
                "tense": tense,
                "number": number,
                "verbType": verbType,
                "gender": gender
            })

        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(sentence)

        if sentence.endswith("?"):
            intent = "Question"
        elif any(word.lower() in ["please", "kindly"] for word in tokens):
            intent = "Polite Command"
        elif tokens and tokens[0].lower() in ["do", "make", "go", "run", "close", "open"] and posTags[0][1] == "VB":
            intent = "Imperative"
        else:
            intent = "Statement"

        return {
            "tokens": result,
            "sentiment": sentiment,
            "intent": intent
        }

class NLPModule(QWidget):
    def __init__(self):
        super().__init__()
        self.animation = None
        self.setWindowTitle("NLP Analyzer")
        self.setGeometry(100, 100, 850, 500)

        self.mainLayout = QVBoxLayout()

        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter a sentence...")
        self.inputField.returnPressed.connect(self.analyzeInput)

        self.analysisTable = QTableWidget()
        self.analysisTable.setColumnCount(6)
        self.analysisTable.setHorizontalHeaderLabels([
            "Word", "Part-of-speech", "Tense", "Number", "Verb Type", "Gender"
        ])
        self.analysisTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.analysisTable.resizeColumnsToContents()

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(50)
        self.progressBar.setRange(0, 100)
        self.progressBar.setFormat("NORMAL SENTENCE")
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setStyleSheet(
            """
            QProgressBar::chunk {
                border-radius: 8px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9E9E9E, stop:1 #BDBDBD
                );
            }
            """
        )
        self.progressBar.setTextVisible(True)

        self.mainLayout.addWidget(QLabel("Input Sentence:"))
        self.mainLayout.addWidget(self.inputField)
        self.mainLayout.addWidget(QLabel("PARTS OF SPEECH"))
        self.mainLayout.addWidget(self.analysisTable)
        self.mainLayout.addWidget(QLabel("Sentence Type"))
        self.mainLayout.addWidget(self.progressBar)

        self.setLayout(self.mainLayout)

    def analyzeInput(self):
        sentence = self.inputField.text()
        if not sentence:
            return

        result = Helpers.analyzeSentence(sentence)

        self.analysisTable.setRowCount(0)

        for i, token in enumerate(result["tokens"]):
            self.analysisTable.insertRow(i)
            self.analysisTable.setItem(i, 0, QTableWidgetItem(token["word"]))
            self.analysisTable.setItem(i, 1, QTableWidgetItem(token["partOfSpeech"]))
            self.analysisTable.setItem(i, 2, QTableWidgetItem(token["tense"]))
            self.analysisTable.setItem(i, 3, QTableWidgetItem(token["number"]))
            self.analysisTable.setItem(i, 4, QTableWidgetItem(token["verbType"]))
            self.analysisTable.setItem(i, 5, QTableWidgetItem(token["gender"]))

        compound = result["sentiment"]["compound"]
        progress = int((compound + 1) * 50)

        if compound > 0:
            chunkStyle = """
                QProgressBar::chunk {
                    border-radius: 8px;
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4CAF50, stop:1 #81C784
                    );
                }
                """
            self.progressBar.setFormat("POSITIVE SENTENCE")
        elif compound < 0:
            chunkStyle = """
                QProgressBar::chunk {
                    border-radius: 8px;
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #F44336, stop:1 #E57373
                    );
                }
                """
            self.progressBar.setFormat("NEGATIVE SENTENCE")
        else:
            chunkStyle = """
                QProgressBar::chunk {
                    border-radius: 8px;
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #9E9E9E, stop:1 #BDBDBD
                    );
                }
                """
            self.progressBar.setFormat("NORMAL SENTENCE")

        animation = QPropertyAnimation(self.progressBar, b"value")
        animation.setDuration(900)  # 0.6 seconds
        animation.setStartValue(self.progressBar.value())
        animation.setEndValue(progress)
        animation.setEasingCurve(QEasingCurve.Type.CosineCurve)
        animation.start()
        self.animation = animation  # prevent garbage collection

        self.progressBar.setStyleSheet(chunkStyle)

        self.analysisTable.resizeColumnsToContents()