import json
import os
import urllib.parse

from PyQt6.QtWidgets import (
    QMainWindow, QLineEdit, QPushButton, QProgressBar,
    QLabel, QWidget, QVBoxLayout, QHBoxLayout, QMenu,
    QFileDialog, QMessageBox,
)
from PyQt6.QtCore import QUrl, Qt

from .tab_widget import TabWidget
from .history_dialog import HistoryDialog
from .bookmarks_manager import BookmarksManager
from .bookmarks_bar import BookmarksBar
from .find_bar import FindBar
from .download_manager import DownloadManager
from .session_manager import SessionManager
from .extensions_manager import ExtensionsManager
from .extensions_dialog import ExtensionsDialog
from .ad_blocker import AdBlockerInterceptor
from .reader_mode import ReaderMode
from .settings_dialog import SettingsDialog, load_config


class BrowserWindow(QMainWindow):
    def __init__(self, session_urls=None):
        super().__init__()
        self.setWindowTitle("CowxBrowser")
        self.resize(1200, 800)

        self.bookmarks = BookmarksManager()
        self.download_mgr = DownloadManager(self)
        self.session_mgr = SessionManager()
        self.current_theme = "dark"

        self.tabs = TabWidget(self)
        self.extensions_mgr = None

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav = self._build_nav_bar()
        layout.addWidget(nav)

        self._build_bookmarks_bar()
        layout.addWidget(self.bookmarks_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("LoadingProgress")
        self.progress_bar.setMaximumHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        layout.addWidget(self.tabs, 1)

        self.find_bar = FindBar(self)
        self.find_bar.hide()
        layout.addWidget(self.find_bar)

        self.setCentralWidget(central)

        self._setup_tabs(session_urls)
        self._connect_signals()
        self._init_ad_blocker()

    def _setup_tabs(self, session_urls):
        if not session_urls:
            return
        first = True
        for url in session_urls:
            if first:
                wv = self.tabs.widget(self.tabs.currentIndex())
                if wv:
                    wv.setUrl(QUrl(url))
                first = False
            else:
                self.tabs.add_new_tab(url)

    def _build_nav_bar(self):
        nav = QWidget()
        nav.setObjectName("NavBar")
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(4)

        self.back_btn = QPushButton("◀")
        self.back_btn.setToolTip("Back")
        self.back_btn.clicked.connect(self.tabs.navigate_back)
        layout.addWidget(self.back_btn)

        self.forward_btn = QPushButton("▶")
        self.forward_btn.setToolTip("Forward")
        self.forward_btn.clicked.connect(self.tabs.navigate_forward)
        layout.addWidget(self.forward_btn)

        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.setToolTip("Refresh")
        self.refresh_btn.clicked.connect(self.tabs.refresh)
        layout.addWidget(self.refresh_btn)

        layout.addSpacing(6)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL…")
        self.url_bar.returnPressed.connect(self._navigate)
        layout.addWidget(self.url_bar, 1)

        layout.addSpacing(4)

        self.bookmark_btn = QPushButton("☆")
        self.bookmark_btn.setToolTip("Bookmark this page")
        self.bookmark_btn.clicked.connect(self._toggle_bookmark)
        layout.addWidget(self.bookmark_btn)

        self.zoom_indicator = QLabel("100%")
        self.zoom_indicator.setFixedWidth(36)
        self.zoom_indicator.setToolTip("Zoom level")
        layout.addWidget(self.zoom_indicator)

        self.menu_btn = QPushButton("☰")
        self.menu_btn.setToolTip("Menu")
        self.menu_btn.clicked.connect(self._show_hamburger_menu)
        layout.addWidget(self.menu_btn)

        self._hamburger_menu = self._build_hamburger_menu()

        return nav

    def _build_hamburger_menu(self):
        menu = QMenu(self)

        act_history = menu.addAction("📋  History")
        act_history.triggered.connect(self._show_history)

        act_downloads = menu.addAction("⬇  Downloads")
        act_downloads.triggered.connect(self.download_mgr.show)

        act_devtools = menu.addAction("🔧  DevTools")
        act_devtools.triggered.connect(self.tabs.open_devtools)

        act_extensions = menu.addAction("🧩  Extensions…")
        act_extensions.triggered.connect(self._show_extensions)

        act_find = menu.addAction("🔍  Find in Page…")
        act_find.setShortcut("Ctrl+F")
        act_find.triggered.connect(self._show_find_bar)

        act_reader = menu.addAction("📖  Reader Mode")
        act_reader.triggered.connect(self._toggle_reader_mode)

        menu.addSeparator()

        self._zoom_menu = menu.addMenu("🔍  Zoom")
        self._zoom_menu.setObjectName("ZoomMenu")

        self._zoom_current = self._zoom_menu.addAction("100%")
        self._zoom_current.setEnabled(False)

        self._zoom_menu.addSeparator()

        act_zoom_in = self._zoom_menu.addAction("Zoom In")
        act_zoom_in.setShortcut("Ctrl++")
        act_zoom_in.triggered.connect(self._zoom_in)

        act_zoom_out = self._zoom_menu.addAction("Zoom Out")
        act_zoom_out.setShortcut("Ctrl+-")
        act_zoom_out.triggered.connect(self._zoom_out)

        act_zoom_reset = self._zoom_menu.addAction("Reset Zoom")
        act_zoom_reset.setShortcut("Ctrl+0")
        act_zoom_reset.triggered.connect(self._zoom_reset)

        menu.addSeparator()

        self._theme_action = menu.addAction("☀  Toggle Theme")
        self._theme_action.triggered.connect(self._toggle_theme)

        menu.addSeparator()

        data_menu = menu.addMenu("📦  Data")
        act_export_bm = data_menu.addAction("📤 Export Bookmarks")
        act_export_bm.triggered.connect(self._export_bookmarks)
        act_import_bm = data_menu.addAction("📥 Import Bookmarks")
        act_import_bm.triggered.connect(self._import_bookmarks)
        data_menu.addSeparator()
        act_export_hist = data_menu.addAction("📤 Export History")
        act_export_hist.triggered.connect(self._export_history)
        data_menu.addSeparator()
        act_clear_cache = data_menu.addAction("🧹 Clear Cache")
        act_clear_cache.triggered.connect(self._clear_cache)
        act_clear_cookies = data_menu.addAction("🧹 Clear Cookies")
        act_clear_cookies.triggered.connect(self._clear_cookies)

        menu.addSeparator()

        act_settings = menu.addAction("⚙  Settings")
        act_settings.triggered.connect(self._show_settings)

        menu.addSeparator()

        act_adblock = menu.addAction("🛡  Ad Block: ON")
        act_adblock.setCheckable(True)
        act_adblock.setChecked(True)
        act_adblock.triggered.connect(self._toggle_ad_block)

        return menu

    def _show_hamburger_menu(self):
        self._update_zoom_menu_text()
        btn = self.menu_btn
        self._hamburger_menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def _toggle_reader_mode(self):
        wv = self.tabs.current_webview()
        if wv:
            ReaderMode.toggle(wv)

    def _export_bookmarks(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Bookmarks", "bookmarks.json", "JSON (*.json)")
        if not path:
            return
        data = [b.to_dict() for b in self.bookmarks.get_all()]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _import_bookmarks(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Bookmarks", "", "JSON (*.json)")
        if not path:
            return
        try:
            with open(path) as f:
                data = json.load(f)
            for item in data:
                self.bookmarks.add(item.get("url", ""), item.get("title", ""))
            self.bookmarks_bar.refresh()
            QMessageBox.information(self, "Import", "Bookmarks imported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Import Error", str(e))

    def _export_history(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export History", "history.json", "JSON (*.json)")
        if not path:
            return
        data = [e.to_dict() for e in self.tabs.history.get_all()]
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _clear_cache(self):
        profile = self._get_profile()
        if profile:
            profile.clearHttpCache()
            QMessageBox.information(self, "Cache Cleared", "HTTP cache has been cleared.")

    def _clear_cookies(self):
        profile = self._get_profile()
        if profile:
            profile.cookieStore().deleteAllCookies()
            QMessageBox.information(self, "Cookies Cleared", "All cookies have been deleted.")

    def _init_ad_blocker(self):
        profile = self._get_profile()
        if profile:
            self._ad_blocker = AdBlockerInterceptor()
            profile.setUrlRequestInterceptor(self._ad_blocker)

    def _toggle_ad_block(self, checked):
        profile = self._get_profile()
        if profile:
            if checked:
                profile.setUrlRequestInterceptor(self._ad_blocker)
            else:
                profile.setUrlRequestInterceptor(None)

    def _zoom_in(self):
        pct = int(self.tabs.get_zoom() * 100)
        val = min(300, pct + 10)
        self.tabs.set_zoom(val / 100.0)

    def _zoom_out(self):
        pct = int(self.tabs.get_zoom() * 100)
        val = max(25, pct - 10)
        self.tabs.set_zoom(val / 100.0)

    def _zoom_reset(self):
        self.tabs.set_zoom(1.0)

    def _update_zoom_display(self, factor: float):
        pct = int(round(factor * 100))
        self.zoom_indicator.setText(f"{pct}%")
        self._zoom_current.setText(f"{pct}%")

    def _update_zoom_menu_text(self):
        pct = int(self.tabs.get_zoom() * 100)
        self._zoom_current.setText(f"{pct}%")
        self.zoom_indicator.setText(f"{pct}%")

    def _build_bookmarks_bar(self):
        self.bookmarks_bar = BookmarksBar(self.bookmarks, self._navigate_to_url, self)
        self.bookmarks_bar.setObjectName("BookmarksBar")
        self.bookmarks_bar.setStyleSheet("")

    def _connect_signals(self):
        self.tabs.url_changed.connect(self._update_url_bar)
        self.tabs.title_changed.connect(self.setWindowTitle)
        self.tabs.back_forward_changed.connect(self._update_nav_buttons)
        self.tabs.zoom_changed.connect(self._update_zoom_display)
        self.tabs.load_progress.connect(self._update_progress_bar)

        profile = self._get_profile()
        if profile:
            profile.downloadRequested.connect(self.download_mgr.handle_download)
            self.extensions_mgr = ExtensionsManager(profile, parent=self)

    def _update_progress_bar(self, progress: int):
        if progress <= 0 or progress >= 100:
            self.progress_bar.hide()
        else:
            self.progress_bar.setValue(progress)
            self.progress_bar.show()

    def _navigate(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        wv = self.tabs.current_webview()
        if wv:
            url = QUrl(text)
            if url.scheme():
                wv.setUrl(url)
            elif "." in text and " " not in text:
                wv.setUrl(QUrl("https://" + text))
            else:
                config = load_config()
                engine = config.get("search_engine", "duckduckgo")
                search_url = SettingsDialog.get_search_url(text, engine)
                wv.setUrl(QUrl(search_url))

    def _update_url_bar(self, url: QUrl):
        self.url_bar.setText(url.toString())
        url_str = url.toString()
        if self.bookmarks.is_bookmarked(url_str):
            self.bookmark_btn.setText("★")
            self.bookmark_btn.setToolTip("Remove bookmark")
        else:
            self.bookmark_btn.setText("☆")
            self.bookmark_btn.setToolTip("Bookmark this page")

    def _update_nav_buttons(self, can_back: bool, can_forward: bool):
        self.back_btn.setEnabled(can_back)
        self.forward_btn.setEnabled(can_forward)

    def _get_profile(self):
        wv = self.tabs.current_webview()
        return wv.page().profile() if wv else None

    def _toggle_bookmark(self):
        wv = self.tabs.current_webview()
        if not wv:
            return
        url = wv.url().toString()
        if self.bookmarks.is_bookmarked(url):
            self.bookmarks.remove(url)
            self.bookmark_btn.setText("☆")
            self.bookmark_btn.setToolTip("Bookmark this page")
        else:
            self.bookmarks.add(url, wv.page().title() or url)
            self.bookmark_btn.setText("★")
            self.bookmark_btn.setToolTip("Remove bookmark")
        self.bookmarks_bar.refresh()

    def _show_history(self):
        dialog = HistoryDialog(self.tabs.history, self)
        dialog.navigated.connect(self._navigate_to_url)
        dialog.exec()

    def _navigate_to_url(self, url: QUrl):
        wv = self.tabs.current_webview()
        if wv:
            wv.setUrl(url)

    def _toggle_theme(self):
        from PyQt6.QtWidgets import QApplication
        from .theme import DARK_THEME, LIGHT_THEME

        app = QApplication.instance()
        if not app:
            return
        if self.current_theme == "dark":
            app.setStyleSheet(LIGHT_THEME)
            self._theme_action.setText("🌙  Toggle Theme")
            self.current_theme = "light"
        else:
            app.setStyleSheet(DARK_THEME)
            self._theme_action.setText("☀  Toggle Theme")
            self.current_theme = "dark"

    def _show_find_bar(self):
        self.find_bar.set_page(self.tabs.current_page())
        self.find_bar.show()
        self.find_bar.focus()

    def _show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def _show_extensions(self):
        if not self.extensions_mgr:
            profile = self._get_profile()
            if not profile:
                return
            self.extensions_mgr = ExtensionsManager(profile, parent=self)
        dialog = ExtensionsDialog(self.extensions_mgr, self)
        dialog.exec()

    def keyPressEvent(self, event):
        mod = event.modifiers()
        key = event.key()

        if key == Qt.Key.Key_D and mod & Qt.KeyboardModifier.ControlModifier:
            self._toggle_bookmark()
            return
        if key == Qt.Key.Key_W and mod & Qt.KeyboardModifier.ControlModifier:
            self.tabs.close_current_tab()
            return
        if key == Qt.Key.Key_T and mod & Qt.KeyboardModifier.ControlModifier:
            self.tabs.add_new_tab()
            return
        if key == Qt.Key.Key_R and mod & Qt.KeyboardModifier.ControlModifier:
            self.tabs.refresh()
            return
        if key == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
            return

        super().keyPressEvent(event)

    def closeEvent(self, event):
        urls = self.tabs.get_all_urls()
        pinned = self.tabs.get_pinned_urls()
        zoom = self.tabs.get_site_zoom()
        self.session_mgr.save(urls, pinned=pinned, zoom=zoom)
        super().closeEvent(event)
