import json
import os

from PyQt6.QtCore import QObject, pyqtSignal


EXTENSIONS_FILE = os.path.expanduser("~/.cowxbrowser/extensions.json")

BUILTIN_EXTENSIONS = ("chromium-pdf", "Google Hangouts")


class ExtensionsManager(QObject):
    loaded = pyqtSignal(str, str)
    unloaded = pyqtSignal(str)

    def __init__(self, profile, path: str = EXTENSIONS_FILE, parent=None):
        super().__init__(parent)
        self._path = path
        self._mgr = profile.extensionManager()
        self._loaded_paths: list[str] = []

        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._restore()

    def _restore(self):
        try:
            with open(self._path) as f:
                data = json.load(f)
                paths = data if isinstance(data, list) else data.get("paths", [])
        except Exception:
            paths = []
        for p in paths:
            if os.path.isdir(p):
                self._loaded_paths.append(p)
                self._mgr.loadExtension(p)

    def _save(self):
        paths = [p for p in self._loaded_paths if os.path.isdir(p)]
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w") as f:
            json.dump({"paths": paths}, f, indent=2)

    def load_extension(self, path: str) -> bool:
        if not os.path.isdir(path) or not os.path.isfile(os.path.join(path, "manifest.json")):
            return False
        if path in self._loaded_paths:
            return False
        self._loaded_paths.append(path)
        self._mgr.loadExtension(path)
        self._save()
        return True

    def unload_extension(self, name: str):
        if name in BUILTIN_EXTENSIONS:
            return
        self._mgr.unloadExtension(name)
        for i, p in enumerate(self._loaded_paths):
            mf = os.path.join(p, "manifest.json")
            if os.path.isfile(mf):
                try:
                    with open(mf) as f:
                        m = json.load(f)
                    if m.get("name") == name:
                        self._loaded_paths.pop(i)
                        break
                except Exception:
                    continue
        self._save()

    def set_enabled(self, name: str, enabled: bool):
        if name in BUILTIN_EXTENSIONS:
            return
        self._mgr.setExtensionEnabled(name, enabled)

    def get_extensions(self) -> list:
        return list(self._mgr.extensions())
