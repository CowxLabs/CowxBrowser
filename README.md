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

### Quick start (Linux)

```bash
curl -L https://github.com/CowxLabs/CowxBrowser/releases/download/v0.1.0-alpha/install.py | python3
cowxbrowser
```

### All options

See the full **[Installation Guide](INSTALL.md)** for:

- Standalone binary (Linux, no Python needed)
- From source (Linux / macOS / Windows)
- Distribution archive
- Updating, uninstalling, and troubleshooting

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

## Building from Source

```bash
git clone https://github.com/CowxLabs/CowxBrowser.git
cd CowxBrowser
make build     # builds standalone binary
make run       # runs from source
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
