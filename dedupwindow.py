"""dedupwindow.py：流式去重（基线：全部记住，无窗口、无持久化）。"""
from __future__ import annotations


class Dedup:
    def __init__(self, window: int = 5, expected: int = 1000):
        self.window = window
        self.expected = expected
        self.seen = set()
        self.accepted = 0
        self.duplicates = 0
        self.expired = 0
        self.wal = []

    def offer(self, event_id: str, at: int) -> dict:
        """基线：全局集合判重，永不过期。"""
        if event_id in self.seen:
            self.duplicates += 1
            return {"accepted": False, "reason": "duplicate"}
        self.seen.add(event_id)
        self.accepted += 1
        self.wal.append(("offer", event_id, at))
        return {"accepted": True}

    def sweep(self, now: int) -> dict:
        raise NotImplementedError("窗口淘汰还没实现")

    def restore(self) -> int:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"accepted": self.accepted, "duplicates": self.duplicates, "expired": self.expired,
                "seen": len(self.seen), "window": self.window, "expected": self.expected}
