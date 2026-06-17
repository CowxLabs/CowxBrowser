import json
import os

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QLineEdit, QSpinBox, QTabWidget,
    QWidget, QFormLayout, QGroupBox,
)

CONFIG_FILE = os.path.expanduser("~/.cowxbrowser/config.json")

SEARCH_ENGINES = {
    "duckduckgo": "https://duckduckgo.com/?q={}",
    "google": "https://www.google.com/search?q={}",
    "bing": "https://www.bing.com/search?q={}",
    "brave": "https://search.brave.com/search?q={}",
}


def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return {}


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(480, 360)
        self.setObjectName("SettingsDialog")

        config = load_config()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        general = QWidget()
        general_layout = QFormLayout(general)
        general_layout.setSpacing(10)

        self.homepage = QLineEdit(config.get("homepage", "https://duckduckgo.com"))
        general_layout.addRow("Homepage:", self.homepage)

        self.search_engine = QComboBox()
        for name in SEARCH_ENGINES:
            self.search_engine.addItem(name.capitalize(), name)
        current_se = config.get("search_engine", "duckduckgo")
        idx = self.search_engine.findData(current_se)
        if idx >= 0:
            self.search_engine.setCurrentIndex(idx)
        general_layout.addRow("Search engine:", self.search_engine)

        self.default_zoom = QSpinBox()
        self.default_zoom.setRange(25, 300)
        self.default_zoom.setSuffix("%")
        self.default_zoom.setValue(config.get("default_zoom", 100))
        general_layout.addRow("Default zoom:", self.default_zoom)

        tabs.addTab(general, "General")

        about = QWidget()
        about_layout = QVBoxLayout(about)
        about_label = QLabel(
            "<b>CowxBrowser</b><br><br>"
            "Version: 0.1.0-alpha<br><br>"
            "Built with PyQt6 and Qt WebEngine.<br><br>"
            "All data is stored locally in ~/.cowxbrowser/<br>"
            "No telemetry. No tracking."
        )
        about_label.setWordWrap(True)
        about_layout.addWidget(about_label)
        about_layout.addStretch()
        tabs.addTab(about, "About")

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save")
        save_btn.setObjectName("PrimaryButton")
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _save(self):
        config = load_config()
        config["homepage"] = self.homepage.text().strip() or "https://duckduckgo.com"
        config["search_engine"] = self.search_engine.currentData()
        config["default_zoom"] = self.default_zoom.value()
        save_config(config)
        self.accept()

    @staticmethod
    def get_search_url(query: str, engine: str = "duckduckgo") -> str:
        tmpl = SEARCH_ENGINES.get(engine, SEARCH_ENGINES["duckduckgo"])
        import urllib.parse
        return tmpl.format(urllib.parse.quote(query))
