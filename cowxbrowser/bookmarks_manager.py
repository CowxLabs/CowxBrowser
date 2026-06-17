import json
import os
from datetime import datetime


BOOKMARKS_FILE = os.path.expanduser("~/.cowxbrowser/bookmarks.json")


class Bookmark:
    def __init__(self, url: str, title: str, timestamp: str):
        self.url = url
        self.title = title
        self.timestamp = timestamp

    def to_dict(self):
        return {"url": self.url, "title": self.title, "timestamp": self.timestamp}

    @staticmethod
    def from_dict(data):
        return Bookmark(data["url"], data["title"], data["timestamp"])


class BookmarksManager:
    def __init__(self, path: str = BOOKMARKS_FILE):
        self.path = path
        self._entries: list[Bookmark] = []
        self._urls: set[str] = set()
        self._load()

    def add(self, url: str, title: str):
        if not url or url in self._urls:
            return
        self._urls.add(url)
        entry = Bookmark(url, title or url, datetime.now().isoformat())
        self._entries.append(entry)
        self._save()

    def remove(self, url: str):
        self._entries = [e for e in self._entries if e.url != url]
        self._urls.discard(url)
        self._save()

    def is_bookmarked(self, url: str) -> bool:
        return url in self._urls

    def get_all(self) -> list[Bookmark]:
        return list(self._entries)

    def _load(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    data = json.load(f)
                    for item in data:
                        entry = Bookmark.from_dict(item)
                        self._entries.append(entry)
                        self._urls.add(entry.url)
            except (json.JSONDecodeError, KeyError):
                self._entries = []

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump([e.to_dict() for e in self._entries], f, indent=2)
