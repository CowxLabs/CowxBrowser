import json
import os


SESSION_FILE = os.path.expanduser("~/.cowxbrowser/session.json")


class SessionManager:
    def __init__(self, path: str = SESSION_FILE):
        self.path = path

    def save(self, urls: list[str], pinned: list[str] | None = None, zoom: dict[str, float] | None = None):
        data = {"tabs": urls}
        if pinned:
            data["pinned"] = pinned
        if zoom:
            data["zoom"] = zoom
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def restore(self) -> tuple:
        if not os.path.exists(self.path):
            return ["https://duckduckgo.com"], [], {}
        try:
            with open(self.path) as f:
                data = json.load(f)
                tabs = data.get("tabs", [])
                pinned = data.get("pinned", [])
                zoom = data.get("zoom", {})
                return (
                    tabs if tabs else ["https://duckduckgo.com"],
                    pinned if isinstance(pinned, list) else [],
                    zoom if isinstance(zoom, dict) else {},
                )
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return ["https://duckduckgo.com"], [], {}

    def has_session(self) -> bool:
        return os.path.exists(self.path)
