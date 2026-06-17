from urllib.parse import urlparse

from PyQt6.QtWidgets import QTabWidget, QPushButton, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, Qt, pyqtSignal

from .history_manager import HistoryManager


class BrowserWebView(QWebEngineView):
    new_tab_requested = pyqtSignal(object)

    def __init__(self, tab_widget=None):
        super().__init__()
        self._tab_widget = tab_widget

    def createWindow(self, _type):
        if self._tab_widget:
            return self._tab_widget.add_new_tab()
        return BrowserWebView()


class TabWidget(QTabWidget):
    url_changed = pyqtSignal(QUrl)
    title_changed = pyqtSignal(str)
    back_forward_changed = pyqtSignal(bool, bool)
    zoom_changed = pyqtSignal(float)
    load_progress = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = HistoryManager()
        self._zoom_factors: dict[int, float] = {}
        self._site_zoom: dict[str, float] = {}
        self._devtools_windows: dict[int, tuple] = {}
        self._pinned: set[int] = set()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self._close_tab)
        self.currentChanged.connect(self._on_tab_changed)
        self.tabBar().tabMoved.connect(self._sync_pinned_move)

        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(28, 28)
        plus_btn.clicked.connect(lambda: self.add_new_tab())
        self.setCornerWidget(plus_btn)

        self.add_new_tab()

    def add_new_tab(self, url: str = "https://duckduckgo.com") -> BrowserWebView:
        webview = BrowserWebView(tab_widget=self)
        webview.setUrl(QUrl(url))
        self._setup_webview(webview)
        index = self.addTab(webview, "Loading...")
        self._zoom_factors[id(webview)] = self._site_zoom.get(urlparse(url).netloc, 1.0)
        webview.setZoomFactor(self._zoom_factors[id(webview)])
        self.setCurrentIndex(index)
        return webview

    def _setup_webview(self, webview):
        s = webview.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)

        webview.titleChanged.connect(self._make_title_handler(webview))
        webview.urlChanged.connect(self._make_url_handler(webview))
        webview.loadFinished.connect(self._make_load_handler(webview))
        webview.iconChanged.connect(self._make_icon_handler(webview))

        webview.page().loadProgress.connect(lambda p, wv=webview: self._on_page_progress(wv, p))

        webview.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        webview.customContextMenuRequested.connect(self._make_context_handler(webview))

    def close_current_tab(self):
        self._close_tab(self.currentIndex())

    def current_webview(self) -> BrowserWebView | None:
        return self.currentWidget() if self.currentWidget() else None

    def current_page(self) -> QWebEnginePage | None:
        wv = self.current_webview()
        return wv.page() if wv else None

    def get_all_urls(self) -> list[str]:
        urls = []
        for i in range(self.count()):
            wv = self.widget(i)
            if wv:
                urls.append(wv.url().toString())
        return urls

    def get_pinned_urls(self) -> list[str]:
        urls = []
        for i in range(self.count()):
            wv = self.widget(i)
            if wv and id(wv) in self._pinned:
                urls.append(wv.url().toString())
        return urls

    def get_site_zoom(self) -> dict[str, float]:
        return dict(self._site_zoom)

    def set_site_zoom(self, data: dict[str, float]):
        self._site_zoom.update(data)

    def set_pinned_from_urls(self, urls: list[str]):
        for i in range(self.count()):
            wv = self.widget(i)
            if wv and wv.url().toString() in urls:
                self._pinned.add(id(wv))
                self._hide_close_button(i)

    def _hide_close_button(self, index):
        tb = self.tabBar()
        tb.setTabButton(index, tb.ButtonPosition.RightSide, None)

    def _show_close_button(self, index):
        self.setTabsClosable(True)

    def set_zoom(self, factor: float):
        wv = self.current_webview()
        if wv:
            wv.setZoomFactor(factor)
            self._zoom_factors[id(wv)] = factor
            url_str = wv.url().toString()
            domain = urlparse(url_str).netloc
            if domain:
                self._site_zoom[domain] = factor
            self.zoom_changed.emit(factor)

    def get_zoom(self) -> float:
        wv = self.current_webview()
        return wv.zoomFactor() if wv else 1.0

    def open_devtools(self):
        wv = self.current_webview()
        if not wv:
            return
        wid = id(wv)
        if wid in self._devtools_windows:
            existing = self._devtools_windows[wid]
            if existing and existing[0]:
                existing[0].raise_()
                existing[0].activateWindow()
                return

        from PyQt6.QtWidgets import QMainWindow
        from PyQt6.QtWebEngineWidgets import QWebEngineView as DevView

        dev_view = DevView()
        page = wv.page()
        page.setDevToolsPage(dev_view.page())

        win = QMainWindow()
        win.setWindowTitle("DevTools")
        win.resize(800, 600)
        win.setCentralWidget(dev_view)
        win.show()

        win.destroyed.connect(lambda wid=wid: self._devtools_windows.pop(wid, None))

        self._devtools_windows[wid] = (win, dev_view)

    def navigate_back(self):
        wv = self.current_webview()
        if wv:
            wv.page().triggerAction(wv.page().WebAction.Back)

    def navigate_forward(self):
        wv = self.current_webview()
        if wv:
            wv.page().triggerAction(wv.page().WebAction.Forward)

    def refresh(self):
        wv = self.current_webview()
        if wv:
            wv.reload()

    def _close_tab(self, index):
        if self.count() > 1:
            widget = self.widget(index)
            if widget:
                wid = id(widget)
                if wid in self._pinned:
                    return
                self._zoom_factors.pop(wid, None)
                if wid in self._devtools_windows:
                    self._devtools_windows[wid][0].close()
                self._pinned.discard(wid)
            self.removeTab(index)
            if widget:
                widget.deleteLater()

    def _sync_zoom(self):
        wv = self.current_webview()
        if wv:
            factor = self._zoom_factors.get(id(wv), 1.0)
            wv.setZoomFactor(factor)
            self.zoom_changed.emit(factor)

    def _on_tab_changed(self, index):
        wv = self.current_webview()
        if wv:
            self.url_changed.emit(wv.url())
            self._emit_nav_state(wv)
            self._sync_zoom()

    def _emit_nav_state(self, webview):
        try:
            h = webview.page().history()
            self.back_forward_changed.emit(h.canGoBack(), h.canGoForward())
        except Exception:
            self.back_forward_changed.emit(False, False)

    def _sync_pinned_move(self, *_):
        pass

    def _on_page_progress(self, webview, progress):
        if webview == self.current_webview():
            self.load_progress.emit(progress)

    def _make_title_handler(self, webview):
        def handler(title):
            idx = self.indexOf(webview)
            if idx >= 0:
                label = (title[:47] + "…") if len(title) > 50 else (title or "Untitled")
                self.setTabText(idx, label)
                if idx == self.currentIndex():
                    self.title_changed.emit(title or "CowxBrowser")
        return handler

    def _make_url_handler(self, webview):
        def handler(url):
            idx = self.indexOf(webview)
            if idx >= 0 and webview.page():
                if idx == self.currentIndex():
                    self.url_changed.emit(url)
                    self._emit_nav_state(webview)
                self.history.add(
                    url.toString(),
                    webview.page().title() or url.toString(),
                )
                domain = urlparse(url.toString()).netloc
                if domain and domain in self._site_zoom:
                    z = self._site_zoom[domain]
                    self._zoom_factors[id(webview)] = z
                    webview.setZoomFactor(z)
        return handler

    def _make_load_handler(self, webview):
        def handler(ok):
            wid = id(webview)
            if wid in self._zoom_factors:
                webview.setZoomFactor(self._zoom_factors[wid])
        return handler

    def _make_icon_handler(self, webview):
        def handler(icon):
            idx = self.indexOf(webview)
            if idx >= 0:
                self.setTabIcon(idx, icon)
        return handler

    def _make_context_handler(self, webview):
        def handler(pos):
            menu = QMenu()
            data = webview.page().contextMenuData()
            link_url = data.linkUrl() if data else QUrl()
            if link_url.isValid():
                new_tab_action = menu.addAction("🔗 Open Link in New Tab")
                menu.addSeparator()

            wid = id(webview)
            if wid in self._pinned:
                pin_action = menu.addAction("📍 Unpin Tab")
            else:
                pin_action = menu.addAction("📌 Pin Tab")

            menu.addSeparator()
            inspect_action = menu.addAction("🔍 Inspect Element")

            action = menu.exec(webview.mapToGlobal(pos))
            if link_url.isValid() and action == new_tab_action:
                self.add_new_tab(link_url.toString())
            elif action == pin_action:
                self._toggle_pin(webview)
            elif action == inspect_action:
                self.setCurrentWidget(webview)
                self.open_devtools()
        return handler

    def _toggle_pin(self, webview):
        wid = id(webview)
        idx = self.indexOf(webview)
        if idx < 0:
            return
        if wid in self._pinned:
            self._pinned.discard(wid)
        else:
            self._pinned.add(wid)
            self._hide_close_button(idx)
