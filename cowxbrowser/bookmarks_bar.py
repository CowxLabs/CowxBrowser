from PyQt6.QtWidgets import QToolBar, QPushButton, QMenu
from PyQt6.QtCore import QUrl, Qt


class BookmarksBar(QToolBar):
    def __init__(self, bookmarks_manager, navigate_callback, parent=None):
        super().__init__("Bookmarks", parent)
        self.manager = bookmarks_manager
        self.navigate = navigate_callback
        self.setMovable(False)
        self._rebuild()

    def _rebuild(self):
        self.clear()
        for bm in self.manager.get_all():
            label = bm.title[:20] + "…" if len(bm.title) > 20 else bm.title
            btn = QPushButton("📑 " + label)
            btn.setToolTip(bm.url)
            btn.setFlat(True)
            btn.clicked.connect(lambda checked, u=bm.url: self.navigate(QUrl(u)))
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(
                lambda pos, u=bm.url: self._context_menu(pos, u)
            )
            self.addWidget(btn)

    def _context_menu(self, pos, url):
        menu = QMenu(self)
        remove_action = menu.addAction("Remove bookmark")
        action = menu.exec(self.mapToGlobal(pos))
        if action == remove_action:
            self.manager.remove(url)
            self._rebuild()

    def refresh(self):
        self._rebuild()
