# Installing CowxBrowser

## Quick start

**Linux (any distro) — one command:**

```bash
curl -L https://github.com/CowxLabs/CowxBrowser/releases/download/v0.1.0-alpha/install.py | python3
```

Then run: `cowxbrowser`

---

## Option 1: Standalone binary (Linux, no Python needed)

Download the pre-built binary from the [releases page](https://github.com/CowxLabs/CowxBrowser/releases):

```bash
# Download
wget https://github.com/CowxLabs/CowxBrowser/releases/download/v0.1.0-alpha/cowxbrowser-linux-x86_64

# Make executable
chmod +x cowxbrowser-linux-x86_64

# Run
./cowxbrowser-linux-x86_64
```

No dependencies required — the binary bundles Python, PyQt6, and Qt WebEngine.

---

## Option 2: Installer script (Linux, Python required)

The installer script downloads the binary, creates a `~/.local/bin/cowxbrowser` symlink, adds a desktop entry to your app launcher, and configures PATH.

```bash
# Download the installer
wget https://github.com/CowxLabs/CowxBrowser/releases/download/v0.1.0-alpha/install.py

# Run it
python3 install.py
```

After installation:

```bash
cowxbrowser
```

The browser will appear in your application menu as "CowxBrowser".

---

## Option 3: From source (all platforms)

### Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- A virtual environment (recommended)

### Steps

```bash
# Clone the repository
git clone https://github.com/CowxLabs/CowxBrowser.git
cd CowxBrowser

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python -m cowxbrowser.main
```

Or use the Makefile:

```bash
make run
```

---

## Option 4: Distribution archive

The `.tar.gz` archive contains the binary, installer, desktop file, source code, and documentation.

```bash
wget https://github.com/CowxLabs/CowxBrowser/releases/download/v0.1.0-alpha/cowxbrowser-0.1.0-alpha-linux-x86_64.tar.gz
tar xzf cowxbrowser-0.1.0-alpha-linux-x86_64.tar.gz
cd release/
./cowxbrowser
```

---

## Platform notes

### Linux

- Tested on Ubuntu 24.04, Fedora 40, Arch Linux
- Requires `libxcb` and `libgl` (usually pre-installed)
- Binary is built on Ubuntu 24.04 (glibc 2.35+) — if you're on an older distro, use the source installation

### macOS

- Source installation works on macOS 13+
- Binary build coming soon (requires macOS signing)

### Windows

- Source installation works on Windows 10/11
- Binary build coming soon

---

## Verifying the installation

```bash
cowxbrowser --version
# Should print: CowxBrowser 0.1.0-alpha
```

Or just launch it — you should see the browser window with DuckDuckGo as the home page.

---

## Updating

### Binary

Download the latest release binary and replace the old one.

### Source

```bash
cd CowxBrowser
git pull
source venv/bin/activate
pip install -r requirements.txt
```

---

## Uninstalling

### Binary / Installer

```bash
rm ~/.local/bin/cowxbrowser
rm ~/.local/share/applications/cowxbrowser.desktop
rm -rf ~/.cowxbrowser
```

### Source

```bash
rm -rf CowxBrowser
rm -rf ~/.cowxbrowser
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `cowxbrowser: command not found` | Add `~/.local/bin` to your PATH, or re-run the installer |
| Binary won't run (missing libs) | Install system libraries: `sudo apt install libxcb-cursor0 libgl1-mesa-glx` |
| Blank white screen | Try running with `--no-sandbox`: `cowxbrowser --no-sandbox` |
| Qt WebEngine crashes | Ensure your GPU drivers are up to date, or use software rendering: `export QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu"` |
| Fonts look wrong | Install Noto Sans or SF Pro fonts, or use the source installation which falls back to system fonts |

---

Still stuck? [Open an issue](https://github.com/CowxLabs/CowxBrowser/issues/new?labels=bug&template=bug_report.md).
