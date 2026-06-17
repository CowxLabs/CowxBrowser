# CowxBrowser

A barebones lightweight browser built with **PyQt6** and **Qt WebEngine**.

## Features

- Tabbed browsing with drag-and-drop reordering
- Dark and light themes (Catppuccin-inspired)
- Bookmark manager with in-nav toolbar
- Full history with search and clear
- Download manager with progress tracking
- Find in page (Ctrl+F)
- Per-tab zoom with persistent per-site zoom levels
- DevTools (right-click → Inspect Element)
- Session restore (reopens tabs on restart)
- Chrome extension support (Qt built-in extensions)
- Reader mode (CSS-only simplification)
- Ad blocker (blocks ~40 ad/tracker networks)
- Keyboard-driven navigation
- Hamburger menu for clean toolbar

## Installation

### Via pip

```bash
pip install cowxbrowser
```

### From source

```bash
git clone https://github.com/your-username/cowxbrowser.git
cd cowxbrowser
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m cowxbrowser.main
```

### Standalone binary

Download the latest release from the [releases page](https://github.com/your-username/cowxbrowser/releases).

*Linux*: `cowxbrowser-x86_64.AppImage`
*macOS*: `cowxbrowser.dmg`
*Windows*: `cowxbrowser.exe`

## Usage

```
cowxbrowser                              # launch browser
cowxbrowser https://example.com          # open with URL (future)
```

Or from source:

```bash
python -m cowxbrowser.main
python run.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | New tab |
| `Ctrl+W` | Close tab |
| `Ctrl+D` | Bookmark page |
| `Ctrl+R` | Refresh |
| `Ctrl+F` | Find in page |
| `Ctrl++` | Zoom in |
| `Ctrl+-` | Zoom out |
| `Ctrl+0` | Reset zoom |
| `F11`    | Toggle fullscreen |

## Data Storage

All user data is stored in `~/.cowxbrowser/`:

| File | Purpose |
|------|---------|
| `config.json` | Theme preference |
| `bookmarks.json` | Bookmark URLs and titles |
| `history.json` | Browsing history |
| `session.json` | Open tabs, pinned tabs, per-site zoom |
| `extensions.json` | Loaded extension paths |

No data is sent anywhere. Everything stays on your machine.

## Privacy

- **No telemetry.** CowxBrowser does not phone home.
- **No analytics.** No tracking, no usage data.
- **No third-party services.** DuckDuckGo is the default search engine and is only contacted when you search.
- **Ad blocking is opt-out.** Enabled by default, toggle off in the menu.

## Building a Standalone Binary

```bash
pip install pyinstaller
pyinstaller cowxbrowser.spec
```

Output appears in `dist/`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
