from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QListWidget, QDockWidget, QMenuBar, QMenu

from webengine import WebEngineModule
from pdftools import PdfToolsModule
from charts import ChartModule
from qtquickqml import QMLModule
from camera import CameraModule


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.savedUrl = QUrl("https://swordmasters.io/")
        self.setWindowTitle("PySide6 Learning Modules")

        self.pages = QStackedWidget(self)
        self.setCentralWidget(self.pages)
        self.pages.currentChanged.connect(self.onPageChanged)

        self.listWidget = QListWidget(self)
        self.listWidget.currentRowChanged.connect(self.pages.setCurrentIndex)

        self.listDock = QDockWidget(self)
        self.listDock.setWindowTitle("PySide6 Modules")
        self.listDock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.listDock.setWidget(self.listWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.listDock)

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        # <editor-fold desc="QtWebEngine">
        self.webview = WebEngineModule()
        self.pages.addWidget(self.webview)
        self.listWidget.addItem("Web View Demo")
        self.webview.urlChanged.connect(self.updateWebActions)

        self.webMenu = QMenu("Web View")
        self.menubar.addMenu(self.webMenu)

        self.reloadAction = QAction("Reload")
        self.reloadAction.triggered.connect(self.webview.reload)
        self.reloadAction.setShortcut("Ctrl+R")
        self.reloadAction.setStatusTip("Reload")
        self.webMenu.addAction(self.reloadAction)

        self.backAction = QAction("Back")
        self.backAction.triggered.connect(self.webview.back)
        self.backAction.setShortcut("Alt+Left")
        self.backAction.setStatusTip("Back")
        self.webMenu.addAction(self.backAction)

        self.forwardAction = QAction("Forward")
        self.forwardAction.triggered.connect(self.webview.forward)
        self.forwardAction.setShortcut("Alt+Right")
        self.forwardAction.setStatusTip("Forward")
        self.webMenu.addAction(self.forwardAction)
        # </editor-fold>

        # <editor-fold desc="QtPdf">
        self.pdfModule = PdfToolsModule()
        self.pages.addWidget(self.pdfModule)
        self.listWidget.addItem("PDF Tools Demo")

        self.pdfMenu = QMenu("PDF Tools")
        self.menubar.addMenu(self.pdfMenu)

        self.browseAction = QAction("Browse")
        self.browseAction.triggered.connect(self.pdfModule.browseFile)
        self.browseAction.setShortcut("Ctrl+O")
        self.browseAction.setStatusTip("Browse PDF File")
        self.pdfMenu.addAction(self.browseAction)

        self.pdfMenu.addSeparator()

        self.pageModeAction = QActionGroup(self)
        self.pageModeAction.setExclusive(True)

        self.singlePageAction = QAction("View Only Current Page", self, checkable=True)
        self.singlePageAction.triggered.connect(
            lambda: self.pdfModule.pdfView.setPageMode(QPdfView.PageMode.SinglePage)
        )
        self.pdfMenu.addAction(self.singlePageAction)
        self.pageModeAction.addAction(self.singlePageAction)

        self.multiPageAction = QAction("View All Pages", self, checkable=True)
        self.multiPageAction.triggered.connect(
            lambda: self.pdfModule.pdfView.setPageMode(QPdfView.PageMode.MultiPage)
        )
        self.pdfMenu.addAction(self.multiPageAction)
        self.pageModeAction.addAction(self.multiPageAction)

        if self.pdfModule.pdfView.pageMode() == QPdfView.PageMode.SinglePage:
            self.singlePageAction.setChecked(True)
        elif self.pdfModule.pdfView.pageMode() == QPdfView.PageMode.MultiPage:
            self.multiPageAction.setChecked(True)

        self.pdfMenu.addSeparator()

        self.zoomModeAction = QActionGroup(self)
        self.zoomModeAction.setExclusive(True)

        self.fitInViewAction = QAction("Fit In View", self, checkable=True)
        self.fitInViewAction.triggered.connect(
            lambda: self.pdfModule.pdfView.setZoomMode(QPdfView.ZoomMode.FitInView)
        )
        self.pdfMenu.addAction(self.fitInViewAction)
        self.zoomModeAction.addAction(self.fitInViewAction)

        self.fitToWidthAction = QAction("Fit To Width", self, checkable=True)
        self.fitToWidthAction.triggered.connect(
            lambda: self.pdfModule.pdfView.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        )
        self.pdfMenu.addAction(self.fitToWidthAction)
        self.zoomModeAction.addAction(self.fitToWidthAction)

        if self.pdfModule.pdfView.zoomMode() == QPdfView.ZoomMode.FitInView:
            self.fitInViewAction.setChecked(True)
        elif self.pdfModule.pdfView.zoomMode() == QPdfView.ZoomMode.FitToWidth:
            self.fitToWidthAction.setChecked(True)

        self.pdfMenu.addSeparator()
        # </editor-fold>

        self.charts = ChartModule()
        self.pages.addWidget(self.charts)
        self.listWidget.addItem("Charts Demo")

        self.qml = QMLModule(self)
        self.pages.addWidget(self.qml)
        self.listWidget.addItem("Qt Quick & QML Demo")

        self.camera = CameraModule(self)
        self.pages.addWidget(self.camera)
        self.listWidget.addItem("Image Capture Demo")

        self.cameraMenu = QMenu("Camera")
        self.menubar.addMenu(self.cameraMenu)

        self.photoCaptureAction = QAction("Take Photo", self)
        self.photoCaptureAction.triggered.connect(self.camera.takePhoto)
        self.photoCaptureAction.setShortcut('Shift+Alt+2')
        self.photoCaptureAction.setStatusTip("Take Photo")
        self.cameraMenu.addAction(self.photoCaptureAction)

        self.screenCaptureAction = QAction("Take Screenshot", self)
        self.screenCaptureAction.triggered.connect(self.camera.takeScreenshot)
        self.screenCaptureAction.setShortcut('Shift+Alt+5')
        self.screenCaptureAction.setStatusTip("Take Screenshot")
        self.cameraMenu.addAction(self.screenCaptureAction)

        self.onPageChanged()


    def onPageChanged(self):
        if self.pages.currentIndex() == 0:
            self.webview.load(self.savedUrl)
            self.webview.page().setAudioMuted(False)
        else:
            if self.webview.url() != QUrl("about:blank") and self.webview.isLoaded:
                self.savedUrl = self.webview.url()
            self.webview.setUrl(QUrl("about:blank"))
            self.webview.page().setAudioMuted(True)

        if hasattr(self, 'camera'):
            if self.pages.currentIndex() == 4:
                self.camera.camera.start()
            else:
                self.camera.camera.stop()

        self.listWidget.setCurrentRow(self.pages.currentIndex())

    def updateWebActions(self):
        if self.webview.history().canGoBack():
            self.backAction.setEnabled(True)
        else:
            self.backAction.setEnabled(False)
        if self.webview.history().canGoForward():
            self.forwardAction.setEnabled(True)
        else:
            self.forwardAction.setEnabled(False)




