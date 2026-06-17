from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtCore import QUrl, pyqtSignal


class HistoryDialog(QDialog):
    navigated = pyqtSignal(QUrl)

    def __init__(self, history_manager, parent=None):
        super().__init__(parent)
        self.history = history_manager
        self.setWindowTitle("History")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Search history…")
        self.filter_input.textChanged.connect(self._refresh)
        layout.addWidget(self.filter_input)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self._on_item_activated)
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self._clear_history)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self._refresh()

    def _refresh(self):
        self.list_widget.clear()
        query = self.filter_input.text().lower()
        for entry in self.history.get_all():
            if query and query not in entry.title.lower() and query not in entry.url.lower():
                continue
            display = f"{entry.title}  —  {entry.url}"
            self.list_widget.addItem(display)

    def _on_item_activated(self, item):
        text = item.text()
        url_part = text.rsplit("  —  ", 1)[-1]
        self.navigated.emit(QUrl(url_part))
        self.accept()

    def _clear_history(self):
        self.history.clear()
        self._refresh()
