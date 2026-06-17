DARK_THEME = """
QMainWindow, QWidget {
    background-color: #0d0d0f;
    color: #f2f2f7;
    font-family: -apple-system, "SF Pro Text", "Segoe UI", "Noto Sans", sans-serif;
    font-size: 13px;
}

QWidget#NavBar {
    background-color: #0d0d0f;
    border-bottom: 1px solid #1c1c1e;
    min-height: 40px;
}

QWidget#NavBar QPushButton {
    background: transparent;
    color: #98989e;
    border: none;
    border-radius: 6px;
    padding: 0;
    font-size: 15px;
    min-width: 30px;
    min-height: 30px;
}

QWidget#NavBar QPushButton:hover {
    background: rgba(255, 255, 255, 0.07);
    color: #f2f2f7;
}

QWidget#NavBar QPushButton:pressed {
    background: rgba(255, 255, 255, 0.12);
    color: #f2f2f7;
}

QWidget#NavBar QPushButton:disabled {
    color: rgba(255, 255, 255, 0.15);
    background: transparent;
}

QWidget#NavBar QLineEdit {
    background: #1c1c1e;
    color: #f2f2f7;
    border: 1px solid #2e2e32;
    border-radius: 18px;
    padding: 6px 16px;
    font-size: 13px;
    min-height: 24px;
    selection-background-color: #7c5cfc;
    selection-color: #ffffff;
}

QWidget#NavBar QLineEdit:focus {
    border: 1px solid #7c5cfc;
    background: #252529;
}

QWidget#NavBar QLineEdit:hover:!focus {
    border: 1px solid #3a3a3e;
}

QWidget#NavBar QLabel {
    color: #636369;
    font-size: 11px;
    padding: 0 2px;
}

QWidget#NavBar QSlider::groove:horizontal {
    background: #252529;
    height: 3px;
    border-radius: 1.5px;
}

QWidget#NavBar QSlider::handle:horizontal {
    background: #7c5cfc;
    width: 10px;
    height: 10px;
    margin: -3.5px 0;
    border-radius: 5px;
}

QWidget#NavBar QSlider::handle:horizontal:hover {
    background: #9b7dfc;
    width: 12px;
    height: 12px;
    margin: -4.5px 0;
    border-radius: 6px;
}

QWidget#NavBar QSlider::sub-page:horizontal {
    background: #7c5cfc;
    border-radius: 1.5px;
}

QToolBar#BookmarksBar {
    background-color: #0d0d0f;
    border: none;
    border-bottom: 1px solid #1c1c1e;
    padding: 0 8px;
    spacing: 2px;
    min-height: 22px;
}

QToolBar#BookmarksBar QPushButton {
    background: transparent;
    border: none;
    color: #636369;
    font-size: 11px;
    padding: 1px 6px;
    border-radius: 3px;
    min-width: 0;
    min-height: 18px;
}

QToolBar#BookmarksBar QPushButton:hover {
    background: rgba(255, 255, 255, 0.07);
    color: #f2f2f7;
}

QWidget#FindBar {
    background-color: #0d0d0f;
    border-top: 1px solid #1c1c1e;
    min-height: 32px;
}

QWidget#FindBar QLabel {
    color: #636369;
    font-size: 12px;
    padding: 0 4px;
}

QWidget#FindBar QLineEdit {
    background: #1c1c1e;
    color: #f2f2f7;
    border: 1px solid #2e2e32;
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 12px;
    min-height: 20px;
}

QWidget#FindBar QLineEdit:focus {
    border: 1px solid #7c5cfc;
}

QWidget#FindBar QPushButton {
    background: transparent;
    color: #98989e;
    border: none;
    border-radius: 4px;
    padding: 4px 6px;
    font-size: 11px;
    min-width: 24px;
    min-height: 20px;
}

QWidget#FindBar QPushButton:hover {
    background: rgba(255, 255, 255, 0.07);
    color: #f2f2f7;
}

QLineEdit {
    background: #1c1c1e;
    color: #f2f2f7;
    border: 1px solid #2e2e32;
    border-radius: 10px;
    padding: 6px 14px;
    font-size: 13px;
    min-height: 22px;
    selection-background-color: #7c5cfc;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border: 1px solid #7c5cfc;
}

QLineEdit:hover:!focus {
    border: 1px solid #3a3a3e;
}

QPushButton {
    background: #1c1c1e;
    color: #f2f2f7;
    border: 1px solid #2e2e32;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    min-width: 36px;
    min-height: 24px;
}

QPushButton:hover {
    background: #252529;
    border: 1px solid #3a3a3e;
}

QPushButton:pressed {
    background: #7c5cfc;
    color: #ffffff;
    border: 1px solid #7c5cfc;
}

QPushButton:disabled {
    background: #111113;
    color: #2e2e32;
    border: 1px solid #1c1c1e;
}

QSlider::groove:horizontal {
    background: #252529;
    height: 3px;
    border-radius: 1.5px;
}

QSlider::handle:horizontal {
    background: #7c5cfc;
    width: 10px;
    height: 10px;
    margin: -3.5px 0;
    border-radius: 5px;
}

QSlider::handle:horizontal:hover {
    background: #9b7dfc;
    width: 12px;
    height: 12px;
    margin: -4.5px 0;
    border-radius: 6px;
}

QSlider::sub-page:horizontal {
    background: #7c5cfc;
    border-radius: 1.5px;
}

QTabWidget::pane {
    background-color: #0d0d0f;
    border: none;
}

QTabBar {
    background-color: #0d0d0f;
    border: none;
    padding: 0 8px;
}

QTabBar::tab {
    background: transparent;
    color: #636369;
    padding: 6px 14px;
    border: none;
    border-bottom: 2px solid transparent;
    margin-right: 0;
    font-size: 12px;
    min-height: 26px;
}

QTabBar::tab:selected {
    color: #f2f2f7;
    border-bottom: 2px solid #7c5cfc;
}

QTabBar::tab:hover:!selected {
    color: #98989e;
    background: transparent;
    border-bottom: 2px solid #2e2e32;
}

QTabBar::close-button {
    image: none;
    background: #2e2e32;
    border-radius: 7px;
    padding: 0;
    margin: 2px 0 2px 4px;
    min-width: 14px;
    min-height: 14px;
}

QTabBar::close-button:hover {
    background: #f28b82;
}

QDialog {
    background-color: #0d0d0f;
}

QTreeWidget {
    background-color: #0d0d0f;
    color: #f2f2f7;
    border: 1px solid #1c1c1e;
    border-radius: 8px;
    font-size: 13px;
    outline: none;
}

QTreeWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
}

QTreeWidget::item:hover {
    background: rgba(255, 255, 255, 0.04);
}

QTreeWidget::item:selected {
    background: rgba(124, 92, 252, 0.25);
    color: #f2f2f7;
}

QHeaderView::section {
    background-color: transparent;
    color: #636369;
    border: none;
    border-bottom: 1px solid #1c1c1e;
    padding: 8px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

QListWidget {
    background-color: #0d0d0f;
    color: #f2f2f7;
    border: 1px solid #1c1c1e;
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
    outline: none;
}

QListWidget::item {
    padding: 8px 14px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background: rgba(255, 255, 255, 0.04);
}

QListWidget::item:selected {
    background: rgba(124, 92, 252, 0.25);
    color: #f2f2f7;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: rgba(255, 255, 255, 0.08);
    min-height: 30px;
    border-radius: 3px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: rgba(255, 255, 255, 0.15);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: rgba(255, 255, 255, 0.08);
    min-width: 30px;
    border-radius: 3px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: rgba(255, 255, 255, 0.15);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMenu {
    background-color: #1c1c1e;
    color: #f2f2f7;
    border: 1px solid #2e2e32;
    border-radius: 10px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 28px 8px 14px;
    border-radius: 5px;
    font-size: 13px;
}

QMenu::item:selected {
    background: rgba(124, 92, 252, 0.25);
    color: #f2f2f7;
}

QMenu::separator {
    background: #2e2e32;
    height: 1px;
    margin: 4px 8px;
}

QProgressBar {
    background: #1c1c1e;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    font-size: 10px;
    color: transparent;
}

QProgressBar::chunk {
    background: #7c5cfc;
    border-radius: 4px;
}

QProgressBar#LoadingProgress {
    background: transparent;
    border: none;
    border-radius: 0;
    height: 3px;
    text-align: center;
    color: transparent;
}

QProgressBar#LoadingProgress::chunk {
    background: #7c5cfc;
    border-radius: 0;
}
"""

LIGHT_THEME = """
QMainWindow, QWidget {
    background-color: #f2f2f7;
    color: #1c1c1e;
    font-family: -apple-system, "SF Pro Text", "Segoe UI", "Noto Sans", sans-serif;
    font-size: 13px;
}

QWidget#NavBar {
    background-color: #f2f2f7;
    border-bottom: 1px solid #d1d1d6;
    min-height: 40px;
}

QWidget#NavBar QPushButton {
    background: transparent;
    color: #86868b;
    border: none;
    border-radius: 6px;
    padding: 0;
    font-size: 15px;
    min-width: 30px;
    min-height: 30px;
}

QWidget#NavBar QPushButton:hover {
    background: rgba(0, 0, 0, 0.05);
    color: #1c1c1e;
}

QWidget#NavBar QPushButton:pressed {
    background: rgba(0, 0, 0, 0.1);
    color: #1c1c1e;
}

QWidget#NavBar QPushButton:disabled {
    color: rgba(0, 0, 0, 0.15);
    background: transparent;
}

QWidget#NavBar QLineEdit {
    background: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 18px;
    padding: 6px 16px;
    font-size: 13px;
    min-height: 24px;
    selection-background-color: #7c5cfc;
    selection-color: #ffffff;
}

QWidget#NavBar QLineEdit:focus {
    border: 1px solid #7c5cfc;
    background: #ffffff;
}

QWidget#NavBar QLineEdit:hover:!focus {
    border: 1px solid #b8b8bd;
}

QWidget#NavBar QLabel {
    color: #8e8e93;
    font-size: 11px;
    padding: 0 2px;
}

QWidget#NavBar QSlider::groove:horizontal {
    background: #d1d1d6;
    height: 3px;
    border-radius: 1.5px;
}

QWidget#NavBar QSlider::handle:horizontal {
    background: #7c5cfc;
    width: 10px;
    height: 10px;
    margin: -3.5px 0;
    border-radius: 5px;
}

QWidget#NavBar QSlider::handle:horizontal:hover {
    background: #9b7dfc;
    width: 12px;
    height: 12px;
    margin: -4.5px 0;
    border-radius: 6px;
}

QWidget#NavBar QSlider::sub-page:horizontal {
    background: #7c5cfc;
    border-radius: 1.5px;
}

QToolBar#BookmarksBar {
    background-color: #f2f2f7;
    border: none;
    border-bottom: 1px solid #d1d1d6;
    padding: 0 8px;
    spacing: 2px;
    min-height: 22px;
}

QToolBar#BookmarksBar QPushButton {
    background: transparent;
    border: none;
    color: #8e8e93;
    font-size: 11px;
    padding: 1px 6px;
    border-radius: 3px;
    min-width: 0;
    min-height: 18px;
}

QToolBar#BookmarksBar QPushButton:hover {
    background: rgba(0, 0, 0, 0.05);
    color: #1c1c1e;
}

QWidget#FindBar {
    background-color: #f2f2f7;
    border-top: 1px solid #d1d1d6;
    min-height: 32px;
}

QWidget#FindBar QLabel {
    color: #8e8e93;
    font-size: 12px;
    padding: 0 4px;
}

QWidget#FindBar QLineEdit {
    background: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 12px;
    min-height: 20px;
}

QWidget#FindBar QLineEdit:focus {
    border: 1px solid #7c5cfc;
}

QWidget#FindBar QPushButton {
    background: transparent;
    color: #86868b;
    border: none;
    border-radius: 4px;
    padding: 4px 6px;
    font-size: 11px;
    min-width: 24px;
    min-height: 20px;
}

QWidget#FindBar QPushButton:hover {
    background: rgba(0, 0, 0, 0.05);
    color: #1c1c1e;
}

QLineEdit {
    background: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 10px;
    padding: 6px 14px;
    font-size: 13px;
    min-height: 22px;
    selection-background-color: #7c5cfc;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border: 1px solid #7c5cfc;
}

QLineEdit:hover:!focus {
    border: 1px solid #b8b8bd;
}

QPushButton {
    background: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    min-width: 36px;
    min-height: 24px;
}

QPushButton:hover {
    background: #f2f2f7;
    border: 1px solid #b8b8bd;
}

QPushButton:pressed {
    background: #7c5cfc;
    color: #ffffff;
    border: 1px solid #7c5cfc;
}

QPushButton:disabled {
    background: #f8f8fc;
    color: #c7c7cc;
    border: 1px solid #e8e8ec;
}

QSlider::groove:horizontal {
    background: #d1d1d6;
    height: 3px;
    border-radius: 1.5px;
}

QSlider::handle:horizontal {
    background: #7c5cfc;
    width: 10px;
    height: 10px;
    margin: -3.5px 0;
    border-radius: 5px;
}

QSlider::handle:horizontal:hover {
    background: #9b7dfc;
    width: 12px;
    height: 12px;
    margin: -4.5px 0;
    border-radius: 6px;
}

QSlider::sub-page:horizontal {
    background: #7c5cfc;
    border-radius: 1.5px;
}

QTabWidget::pane {
    background-color: #ffffff;
    border: none;
}

QTabBar {
    background-color: #f2f2f7;
    border: none;
    border-bottom: 1px solid #d1d1d6;
    padding: 0 8px;
}

QTabBar::tab {
    background: transparent;
    color: #8e8e93;
    padding: 6px 14px;
    border: none;
    border-bottom: 2px solid transparent;
    margin-right: 0;
    font-size: 12px;
    min-height: 26px;
}

QTabBar::tab:selected {
    color: #1c1c1e;
    border-bottom: 2px solid #7c5cfc;
}

QTabBar::tab:hover:!selected {
    color: #636366;
    background: transparent;
    border-bottom: 2px solid #d1d1d6;
}

QTabBar::close-button {
    image: none;
    background: #c7c7cc;
    border-radius: 7px;
    padding: 0;
    margin: 2px 0 2px 4px;
    min-width: 14px;
    min-height: 14px;
}

QTabBar::close-button:hover {
    background: #f28b82;
}

QDialog {
    background-color: #ffffff;
}

QTreeWidget {
    background-color: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    font-size: 13px;
    outline: none;
}

QTreeWidget::item {
    padding: 8px 12px;
    border-radius: 4px;
}

QTreeWidget::item:hover {
    background: rgba(0, 0, 0, 0.03);
}

QTreeWidget::item:selected {
    background: rgba(124, 92, 252, 0.15);
    color: #1c1c1e;
}

QHeaderView::section {
    background-color: transparent;
    color: #8e8e93;
    border: none;
    border-bottom: 1px solid #d1d1d6;
    padding: 8px 12px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

QListWidget {
    background-color: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
    outline: none;
}

QListWidget::item {
    padding: 8px 14px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background: rgba(0, 0, 0, 0.03);
}

QListWidget::item:selected {
    background: rgba(124, 92, 252, 0.15);
    color: #1c1c1e;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: rgba(0, 0, 0, 0.08);
    min-height: 30px;
    border-radius: 3px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background-color: rgba(0, 0, 0, 0.15);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: rgba(0, 0, 0, 0.08);
    min-width: 30px;
    border-radius: 3px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background-color: rgba(0, 0, 0, 0.15);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMenu {
    background-color: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 10px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 28px 8px 14px;
    border-radius: 5px;
    font-size: 13px;
}

QMenu::item:selected {
    background: rgba(124, 92, 252, 0.15);
    color: #1c1c1e;
}

QMenu::separator {
    background: #d1d1d6;
    height: 1px;
    margin: 4px 8px;
}

QProgressBar {
    background: #e8e8ec;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    font-size: 10px;
    color: transparent;
}

QProgressBar::chunk {
    background: #7c5cfc;
    border-radius: 4px;
}

QProgressBar#LoadingProgress {
    background: transparent;
    border: none;
    border-radius: 0;
    height: 3px;
    text-align: center;
    color: transparent;
}

QProgressBar#LoadingProgress::chunk {
    background: #7c5cfc;
    border-radius: 0;
}
"""
