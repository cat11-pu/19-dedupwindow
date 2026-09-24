"""dedupapi.py：对外门面（老接口 offer 不能改）。"""
from __future__ import annotations

from dedupwindow import Dedup


class Stream:
    def __init__(self, window: int = 5, expected: int = 1000):
        self.dedup = Dedup(window, expected)

    def offer(self, event_id: str, at: int) -> dict:
        return self.dedup.offer(event_id, at)

    def sweep(self, now: int) -> dict:
        return self.dedup.sweep(now)

    def restore(self, blob: bytes = None) -> int:
        return self.dedup.restore()
