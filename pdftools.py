from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog


class PdfToolsModule(QWidget):
    def __init__(self):
        super(PdfToolsModule, self).__init__()

        self.filePath = ""

        self.layout = QVBoxLayout(self)

        self.pdfView = QPdfView(self)
        self.pdfDocument = QPdfDocument(self)
        self.pdfView.setDocument(self.pdfDocument)

        self.pdfView.setPageMode(QPdfView.PageMode.SinglePage)
        self.pdfView.setZoomMode(QPdfView.ZoomMode.FitInView)

        self.layout.addWidget(self.pdfView)

        self.browseButton = QPushButton("Browse", self)
        self.browseButton.clicked.connect(self.browseFile)
        self.layout.addWidget(self.browseButton)

        self.exportButton = QPushButton("Export Page", self)
        self.exportButton.clicked.connect(self.exportFile)
        self.layout.addWidget(self.exportButton)

    def browseFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        self.filePath = filePath
        self.loadPdf()

    def loadPdf(self):
        filePath = self.filePath
        if filePath:
            status = self.pdfDocument.load(filePath)
            if status == QPdfDocument.Status.Ready:
                self.pdfView.setPageMode(QPdfView.PageMode.SinglePage)
                self.pdfView.setZoomMode(QPdfView.ZoomMode.FitInView)

    def exportFile(self):
        if self.pdfDocument.pageCount() > 0:
            filePath, extension = QFileDialog.getSaveFileName(self, "Export Current Page As...", "",
                                                      "PNG image (*.png);;"
                                                      "JPEG image (*.jpg *.jpeg);;"
                                                      "Bitmap image (*.bmp)")
            if filePath:
                currentPage = self.pdfView.pageNavigator().currentPage()
                base = QImage(self.pdfDocument.pagePointSize(currentPage).width(),
                              self.pdfDocument.pagePointSize(currentPage).height(), QImage.Format.Format_ARGB32)
                base.fill(Qt.GlobalColor.white)
                image = self.pdfDocument.render(currentPage, self.pdfDocument.pagePointSize(currentPage).toSize())
                painter = QPainter(base)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
                painter.drawImage(0, 0, image)
                painter.end()
                fileType = extension.split(" ")[-1].replace("*", "").replace("(", "").replace(")", "")
                print(fileType[1:])
                base.save(filePath, fileType[1:].upper())