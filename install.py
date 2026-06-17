#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "CowxLabs/CowxBrowser"
VERSION = "0.1.0-alpha"
BINARY_URL = f"https://github.com/{REPO}/releases/download/v{VERSION}/cowxbrowser-linux-x86_64"


def info(msg):
    print(f"  → {msg}")


def ok(msg):
    print(f"  ✓ {msg}")


def err(msg):
    print(f"  ✗ {msg}", file=sys.stderr)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    print()
    print("  ╔══════════════════════════════╗")
    print("  ║     CowxBrowser Installer    ║")
    print("  ╚══════════════════════════════╝")
    print()

    home = Path.home()
    data_dir = home / ".cowxbrowser"
    bin_dir = home / ".local" / "bin"
    app_dir = data_dir / "app"
    desktop_dir = home / ".local" / "share" / "applications"
    icon_dir = home / ".local" / "share" / "icons" / "hicolor" / "256x256" / "apps"

    info(f"Installing CowxBrowser v{VERSION}")

    # --- detect mode ---
    use_binary = shutil.which("cowxbrowser") is None
    pip_available = shutil.which("pip3") is not None or shutil.which("pip") is not None

    # --- binary install ---
    if use_binary:
        info("Mode: standalone binary")
        app_dir.mkdir(parents=True, exist_ok=True)
        bin_dir.mkdir(parents=True, exist_ok=True)

        binary_path = app_dir / "cowxbrowser"
        if not binary_path.exists():
            import urllib.request

            info(f"Downloading binary from GitHub…")
            try:
                urllib.request.urlretrieve(BINARY_URL, binary_path)
                ok("Downloaded")
            except Exception as e:
                err(f"Download failed: {e}")
                sys.exit(1)

        binary_path.chmod(0o755)

        # Symlink into PATH
        link = bin_dir / "cowxbrowser"
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(binary_path)
        ok(f"Binary installed → {binary_path}")
        ok(f"Symlink created → {link}")
    else:
        info("Mode: pip install (existing binary found)")
        info("Skipping binary download")

    # --- pip install (source deps) ---
    has_pip = shutil.which("pip3") or shutil.which("pip")
    if not use_binary and has_pip:
        info("Installing via pip…")
        pip = shutil.which("pip3") or shutil.which("pip")
        r = run([pip, "install", "--user", "cowxbrowser"])
        if r.returncode == 0:
            ok("pip install done")
        else:
            err(f"pip install failed: {r.stderr}")

    # --- desktop entry ---
    info("Creating desktop entry…")
    desktop_dir.mkdir(parents=True, exist_ok=True)
    icon_dir.mkdir(parents=True, exist_ok=True)

    # Generate icon (simple SVG)
    svg_icon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="32" fill="#1c1c1e"/>
  <circle cx="128" cy="140" r="50" fill="none" stroke="#7c5cfc" stroke-width="8"/>
  <path d="M128 90 Q160 60 190 80 M128 90 Q96 60 66 80 M128 190 Q100 210 80 200" fill="none" stroke="#7c5cfc" stroke-width="6" stroke-linecap="round"/>
  <text x="128" y="224" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#98989e">C</text>
</svg>'''
    icon_path = icon_dir / "cowxbrowser.svg"
    icon_path.write_text(svg_icon)

    desktop = f"""[Desktop Entry]
Name=CowxBrowser
Comment=A barebones lightweight browser
Exec={bin_dir / 'cowxbrowser'} %U
Icon=cowxbrowser
Terminal=false
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;
StartupNotify=true
Keywords=browser;web;qt;
"""
    desktop_path = desktop_dir / "cowxbrowser.desktop"
    desktop_path.write_text(desktop)
    desktop_path.chmod(0o755)

    # Update desktop database
    run(["update-desktop-database", str(desktop_dir)])
    ok("Desktop entry created")

    # --- data directory ---
    data_dir.mkdir(parents=True, exist_ok=True)
    ok(f"Data directory ready → {data_dir}")

    # --- PATH reminder ---
    path_added = False
    rc_files = [home / ".bashrc", home / ".zshrc", home / ".profile"]
    for rc in rc_files:
        if rc.exists() and str(bin_dir) not in rc.read_text():
            with rc.open("a") as f:
                f.write(f'\n# CowxBrowser\nexport PATH="$PATH:{bin_dir}"\n')
            path_added = True
            ok(f"Added {bin_dir} to PATH in {rc.name}")

    print()
    print(f"  ─────────────────────────────────────")
    print(f"  🐮 CowxBrowser v{VERSION} installed!")
    print()
    print(f"  Run:  cowxbrowser")
    if path_added:
        print(f"        (restart your terminal or run: source ~/.bashrc)")
    print(f"  Data: {data_dir}")
    print(f"  Help: cowxbrowser --help")
    print()


if __name__ == "__main__":
    main()
