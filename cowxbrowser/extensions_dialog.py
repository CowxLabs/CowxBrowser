import os

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTreeWidget, QTreeWidgetItem, QFileDialog, QLabel,
    QHeaderView, QMessageBox,
)
from PyQt6.QtCore import Qt


class ExtensionsDialog(QDialog):
    def __init__(self, extensions_manager, parent=None):
        super().__init__(parent)
        self._mgr = extensions_manager
        self.setWindowTitle("Extensions")
        self.setMinimumSize(540, 400)
        self.setObjectName("ExtensionsDialog")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        header = QLabel("Extensions")
        header.setStyleSheet("font-size: 15px; font-weight: 600; padding: 2px 0;")
        layout.addWidget(header)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Extension", "ID", "Enabled"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree, 1)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Load Unpacked")
        add_btn.clicked.connect(self._load_extension)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("Unload Selected")
        remove_btn.clicked.connect(self._unload_extension)
        btn_layout.addWidget(remove_btn)

        btn_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        self._refresh()

    def _refresh(self):
        self.tree.clear()
        for ext in self._mgr.get_extensions():
            name = ext.name()
            eid = ext.id()
            enabled = ext.isEnabled()

            item = QTreeWidgetItem()
            item.setText(0, name)
            item.setText(1, eid)
            item.setText(2, "✓" if enabled else "✗")
            item.setData(0, Qt.ItemDataRole.UserRole, name)
            self.tree.addTopLevelItem(item)

    def _load_extension(self):
        path = QFileDialog.getExistingDirectory(self, "Select extension directory")
        if not path:
            return
        if not os.path.isfile(os.path.join(path, "manifest.json")):
            QMessageBox.warning(self, "Invalid Extension",
                                "No manifest.json found in the selected directory.")
            return
        ok = self._mgr.load_extension(path)
        if ok:
            self._refresh()
        else:
            QMessageBox.information(self, "Extension", "Extension already loaded or invalid.")

    def _unload_extension(self):
        item = self.tree.currentItem()
        if not item:
            return
        name = item.data(0, Qt.ItemDataRole.UserRole)
        self._mgr.unload_extension(name)
        self._refresh()

    def _on_item_clicked(self, item, column):
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if column == 2:
            current = item.text(2) == "✓"
            self._mgr.set_enabled(name, not current)
            self._refresh()
