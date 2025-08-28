import os.path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEnginePermission
from PySide6.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QLineEdit
from pathlib import Path
import json


class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS: {message} (Source: {sourceID}, Line: {lineNumber})")

    def __init__(self, parent: QWebEngineView, profile: QWebEngineProfile):
        super().__init__(profile)

        if os.path.exists(str(Path.home()) + "\\webdata\\permissions.json"):
            with open(str(Path.home()) + "\\webdata\\permissions.json", "r") as f:
                self.savedPermissions = json.load(f)
        else:
            self.savedPermissions = {}

        self.view = parent

        self.setParent(parent)

        self.setAudioMuted(False)

        self.permissionRequested.connect(self.handlePermissions)

    def handlePermissions(self, permission: QWebEnginePermission):
        print(type(permission.permissionType()))
        permissionName = {
            QWebEnginePermission.PermissionType.MediaAudioCapture: "Microphone",
            QWebEnginePermission.PermissionType.MediaVideoCapture: "Camera",
            QWebEnginePermission.PermissionType.MediaAudioVideoCapture: "Microphone + Camera",
            QWebEnginePermission.PermissionType.Geolocation: "Location",
            QWebEnginePermission.PermissionType.Notifications: "Notifications",
            QWebEnginePermission.PermissionType.DesktopVideoCapture: "Screen Sharing (Video)",
            QWebEnginePermission.PermissionType.DesktopAudioVideoCapture: "Screen Sharing (Audio + Video)",
            QWebEnginePermission.PermissionType.MouseLock: "Mouse Lock"
        }.get(permission.permissionType(), "Unknown")

        print(self.savedPermissions)
        if permissionName in self.savedPermissions:
            if self.savedPermissions[permissionName] == "Allow":
                permission.grant()
            else:
                permission.deny()
        else:
            response = QMessageBox(
                self.view,
                text=f"The site {self.url().host()} requests access to your {permissionName}. "
                     f"Do you want to allow this?",
                standardButtons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ).exec_()
            if response == QMessageBox.StandardButton.Yes:
                permission.grant()
            else:
                permission.deny()
            self.savedPermissions[permissionName] = "Allow" if response == QMessageBox.StandardButton.Yes else "Deny"
            with open(str(Path.home()) + "\\webdata\\permissions.json", "w") as f:
                json.dump(self.savedPermissions, f, indent=4)


class WebEngineModule(QWidget):
    def __init__(self):
        super(WebEngineModule, self).__init__()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.updateUrl)
        self.mainLayout.addWidget(self.urlBar)

        self.webview = QWebEngineView()
        self.mainLayout.addWidget(self.webview)

        # <editor-fold desc="Settings">
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # </editor-fold>

        self.userProfile = QWebEngineProfile("User Profile", self.webview)

        print(str(Path.home()) + "\\qtwebcache")

        self.userProfile.setCachePath(str(Path.home()) + "\\qtwebcache")
        self.userProfile.setPersistentStoragePath(str(Path.home()) + "\\webdata")
        self.userProfile.setDownloadPath(str(Path.home()) + "\\Downloads\\qtwebengine")

        self.userProfile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.userProfile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        self.webview.setPage(WebEnginePage(self.webview, self.userProfile))

        self.webview.load("https://www.google.com/")

        self.webview.loadFinished.connect(self.onLoadFinish)
        self.webview.loadStarted.connect(self.onLoadStart)

        self.isLoaded = False


    def onLoadFinish(self):
        self.isLoaded = True

    def onLoadStart(self):
        self.isLoaded = False

    def updateUrl(self):
        url = QUrl(self.urlBar.text())

        # if scheme is blank
        if url.scheme() == "":
            urL = url.toString()
            print(urL)
            if '.' in urL:
                url.setScheme("https")
            else:
                url.setUrl(
                    f'https://www.google.com/search?q={self.urlBar.text()}&oq={self.urlBar.text()}'
                    f'&aqs=chrome..69i57.1409j0j1&sourceid=chrome&ie=UTF-8')

        self.webview.load(url)


