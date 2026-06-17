import sys
import os

# Enable Chrome extensions in Qt WebEngine
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-extensions --no-sandbox"

from PyQt6.QtWidgets import QApplication

from .browser import BrowserWindow
from .theme import DARK_THEME, LIGHT_THEME
from .session_manager import SessionManager
from .settings_dialog import load_config, save_config
from .update_checker import UpdateChecker

VERSION = "0.1.0-alpha"


def main():
    config = load_config()
    theme = config.get("theme", "dark")

    app = QApplication(sys.argv)
    app.setApplicationName("CowxBrowser")
    app.setApplicationVersion(VERSION)

    if theme == "light":
        app.setStyleSheet(LIGHT_THEME)
    else:
        app.setStyleSheet(DARK_THEME)

    session_mgr = SessionManager()
    session_data = session_mgr.restore() if session_mgr.has_session() else None
    if session_data:
        session_urls, pinned_urls, zoom_data = session_data
    else:
        session_urls, pinned_urls, zoom_data = None, [], {}

    window = BrowserWindow(session_urls=session_urls)
    if pinned_urls:
        window.tabs.set_pinned_from_urls(pinned_urls)
    if zoom_data:
        window.tabs.set_site_zoom(zoom_data)
    window.current_theme = theme
    if theme == "light":
        window._theme_action.setText("🌙  Toggle Theme")
    else:
        window._theme_action.setText("☀  Toggle Theme")
    window.show()

    UpdateChecker.check(VERSION, window)

    exit_code = app.exec()

    config["theme"] = window.current_theme
    save_config(config)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
