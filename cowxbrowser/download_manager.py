import os

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, QHBoxLayout, QFileDialog, QHeaderView


class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Downloads")
        self.setMinimumSize(520, 320)
        self.setObjectName("DownloadManager")
        self._downloads: dict = {}

        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["File", "Progress", "Status"])
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.tree)

        btn_layout = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def handle_download(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save Download", download.suggestedFileName())
        if not path:
            download.cancel()
            return

        d = os.path.dirname(path)
        os.makedirs(d, exist_ok=True)

        download.setDownloadDirectory(d)
        download.setDownloadFileName(os.path.basename(path))
        download.accept()

        item = QTreeWidgetItem(self.tree)
        item.setText(0, os.path.basename(path))
        item.setText(1, "0%")
        item.setText(2, "Downloading…")
        self._downloads[id(download)] = (download, item)

        download.receivedBytesChanged.connect(
            lambda: self._update_progress(download)
        )
        download.stateChanged.connect(
            lambda: self._on_state_changed(download)
        )

    def _update_progress(self, download):
        _, item = self._downloads.get(id(download), (None, None))
        if item and download.totalBytes() > 0:
            pct = int(download.receivedBytes() / download.totalBytes() * 100)
            item.setText(1, f"{pct}%")

    def _on_state_changed(self, download):
        _, item = self._downloads.get(id(download), (None, None))
        if not item:
            return
        state = download.state()
        if state == download.DownloadState.DownloadCompleted:
            item.setText(2, "✅ Complete")
        elif state == download.DownloadState.DownloadCancelled:
            item.setText(2, "❌ Cancelled")
        elif state == download.DownloadState.DownloadInterrupted:
            item.setText(2, f"⚠️ {download.interruptReasonString()}")
