import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_imports():
    from cowxbrowser.tab_widget import TabWidget, BrowserWebView
    from cowxbrowser.browser import BrowserWindow
    from cowxbrowser.history_dialog import HistoryDialog
    from cowxbrowser.history_manager import HistoryManager, HistoryEntry
    from cowxbrowser.bookmarks_manager import BookmarksManager, Bookmark
    from cowxbrowser.bookmarks_bar import BookmarksBar
    from cowxbrowser.find_bar import FindBar
    from cowxbrowser.download_manager import DownloadManager
    from cowxbrowser.session_manager import SessionManager
    from cowxbrowser.extensions_manager import ExtensionsManager
    from cowxbrowser.extensions_dialog import ExtensionsDialog
    from cowxbrowser.settings_dialog import SettingsDialog
    from cowxbrowser.ad_blocker import AdBlockerInterceptor
    from cowxbrowser.reader_mode import ReaderMode
    from cowxbrowser.update_checker import UpdateChecker
    from cowxbrowser.theme import DARK_THEME, LIGHT_THEME
    assert DARK_THEME and LIGHT_THEME
    print("All 17 modules imported successfully")


def test_history_manager():
    import tempfile
    from cowxbrowser.history_manager import HistoryManager

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    try:
        hm = HistoryManager(path)
        hm.add("https://example.com", "Example")
        assert len(hm.get_all()) == 1
        hm.clear()
        assert len(hm.get_all()) == 0
    finally:
        os.unlink(path)

    print("HistoryManager OK")


def test_bookmarks_manager():
    import tempfile
    from cowxbrowser.bookmarks_manager import BookmarksManager

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    try:
        bm = BookmarksManager(path)
        bm.add("https://example.com", "Example")
        assert bm.is_bookmarked("https://example.com")
        assert len(bm.get_all()) == 1
        bm.remove("https://example.com")
        assert not bm.is_bookmarked("https://example.com")
    finally:
        os.unlink(path)

    print("BookmarksManager OK")


def test_session_manager():
    import tempfile
    from cowxbrowser.session_manager import SessionManager

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name

    try:
        sm = SessionManager(path)
        sm.save(["https://a.com", "https://b.com"], pinned=["https://a.com"], zoom={"example.com": 1.2})
        urls, pinned, zoom = sm.restore()
        assert urls == ["https://a.com", "https://b.com"]
        assert pinned == ["https://a.com"]
        assert zoom == {"example.com": 1.2}
    finally:
        os.unlink(path)

    print("SessionManager OK")
