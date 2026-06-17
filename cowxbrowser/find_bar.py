from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEnginePage


class FindBar(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FindBar")
        self._page = None
        self._last_text = ""

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        self.label = QLabel("🔍 Find:")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Search in page…")
        self.input.setMinimumWidth(200)
        self.input.textChanged.connect(self._on_text_changed)
        self.input.returnPressed.connect(self._find_next)
        layout.addWidget(self.input)

        self.prev_btn = QPushButton("▲")
        self.prev_btn.setToolTip("Previous")
        self.prev_btn.clicked.connect(self._find_prev)
        layout.addWidget(self.prev_btn)

        self.next_btn = QPushButton("▼")
        self.next_btn.setToolTip("Next")
        self.next_btn.clicked.connect(self._find_next)
        layout.addWidget(self.next_btn)

        self.result_label = QLabel()
        self.result_label.setFixedWidth(100)
        layout.addWidget(self.result_label)

        self.close_btn = QPushButton("✕")
        self.close_btn.setToolTip("Close (Esc)")
        self.close_btn.clicked.connect(self.close_find)
        layout.addWidget(self.close_btn)

    def set_page(self, page: QWebEnginePage | None):
        self._page = page

    def focus(self):
        self.input.setFocus()
        self.input.selectAll()

    def close_find(self):
        self.closed.emit()
        if self._page:
            self._page.findText("")
        self._last_text = ""
        self.input.clear()
        self.result_label.clear()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close_find()
            return
        if event.key() == Qt.Key.Key_Return and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self._find_prev()
            return
        super().keyPressEvent(event)

    def _on_text_changed(self, text):
        self._last_text = text
        self._find(0)

    def _find_next(self):
        self._find(0)

    def _find_prev(self):
        self._find(QWebEnginePage.FindFlag.FindBackward)

    def _find(self, flags):
        if not self._page or not self._last_text:
            return
        self._page.findText(
            self._last_text,
            QWebEnginePage.FindFlag(flags),
            self._on_find_result,
        )

    def _on_find_result(self, found: bool):
        if self._last_text:
            self.result_label.setText("Match found" if found else "No matches")
