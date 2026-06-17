# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).parent

a = Analysis(
    [str(ROOT / "run.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[],
    hiddenimports=[
        "PyQt6",
        "PyQt6.QtWebEngineWidgets",
        "PyQt6.QtWebEngineCore",
        "cowxbrowser",
        "cowxbrowser.main",
        "cowxbrowser.browser",
        "cowxbrowser.tab_widget",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "test", "distutils", "setuptools"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="cowxbrowser",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name="CowxBrowser.app",
    icon=None,
    bundle_identifier="io.github.cowxbrowser",
)
