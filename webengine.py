import os.path

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage, QWebEnginePermission
from PySide6.QtWidgets import QMessageBox
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


class WebEngineModule(QWebEngineView):
    def __init__(self):
        super(WebEngineModule, self).__init__()

        # <editor-fold desc="Settings">
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # </editor-fold>

        self.userProfile = QWebEngineProfile("User Profile", self)

        print(str(Path.home()) + "\\qtwebcache")

        self.userProfile.setCachePath(str(Path.home()) + "\\qtwebcache")
        self.userProfile.setPersistentStoragePath(str(Path.home()) + "\\webdata")
        self.userProfile.setDownloadPath(str(Path.home()) + "\\Downloads\\qtwebengine")

        self.userProfile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.userProfile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        self.setPage(WebEnginePage(self, self.userProfile))

        self.load("https://swordmasters.io/")

        self.loadFinished.connect(self.onLoadFinish)
        self.loadStarted.connect(self.onLoadStart)

        self.isLoaded = False


    def onLoadFinish(self):
        self.isLoaded = True

    def onLoadStart(self):
        self.isLoaded = False


