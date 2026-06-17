import json
import urllib.request
import urllib.error

from PyQt6.QtCore import QThread, pyqtSignal


GITHUB_API = "https://api.github.com/repos/anomalyco/cowxbrowser/releases/latest"


class _UpdateThread(QThread):
    result = pyqtSignal(object)

    def __init__(self, current_version):
        super().__init__()
        self._current = current_version

    def run(self):
        try:
            req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "cowxbrowser"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                latest = data.get("tag_name", "").lstrip("v")
                if latest and latest > self._current.lstrip("v"):
                    self.result.emit({
                        "available": True,
                        "version": latest,
                        "url": data.get("html_url", ""),
                    })
                else:
                    self.result.emit({"available": False})
        except Exception:
            self.result.emit({"available": False})


class UpdateChecker:
    _thread: _UpdateThread | None = None

    @classmethod
    def check(cls, current_version: str, parent_widget):
        if cls._thread is not None:
            return
        cls._thread = _UpdateThread(current_version)
        cls._thread.result.connect(lambda r: cls._on_result(r, parent_widget))
        cls._thread.finished.connect(cls._cleanup)
        cls._thread.start()

    @classmethod
    def _cleanup(cls):
        cls._thread = None

    @classmethod
    def _on_result(cls, result, parent):
        if result.get("available"):
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox(parent)
            msg.setWindowTitle("Update Available")
            msg.setText(f"CowxBrowser {result['version']} is available.")
            msg.setInformativeText("You are running an older version. Download the latest release from GitHub.")
            msg.setStandardButtons(QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Close)
            if msg.exec() == QMessageBox.StandardButton.Open:
                from PyQt6.QtCore import QUrl
                from PyQt6.QtGui import QDesktopServices
                QDesktopServices.openUrl(QUrl(result["url"]))
