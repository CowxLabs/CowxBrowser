import json
import os
from datetime import datetime


HISTORY_FILE = os.path.expanduser("~/.cowxbrowser/history.json")


class HistoryEntry:
    def __init__(self, url: str, title: str, timestamp: str):
        self.url = url
        self.title = title
        self.timestamp = timestamp

    def to_dict(self):
        return {"url": self.url, "title": self.title, "timestamp": self.timestamp}

    @staticmethod
    def from_dict(data):
        return HistoryEntry(data["url"], data["title"], data["timestamp"])


class HistoryManager:
    def __init__(self, path: str = HISTORY_FILE):
        self.path = path
        self._entries: list[HistoryEntry] = []
        self._load()

    def add(self, url: str, title: str):
        if not url or url == "about:blank":
            return
        entry = HistoryEntry(url, title or url, datetime.now().isoformat())
        self._entries.append(entry)
        self._save()

    def get_all(self) -> list[HistoryEntry]:
        return list(reversed(self._entries))

    def clear(self):
        self._entries.clear()
        self._save()

    def _load(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    data = json.load(f)
                    for item in data:
                        entry = HistoryEntry.from_dict(item)
                        self._entries.append(entry)
            except (json.JSONDecodeError, KeyError):
                self._entries = []

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump([e.to_dict() for e in self._entries], f, indent=2)
