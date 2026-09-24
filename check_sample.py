"""把 sample/events.json 跑一遍，打印验收面（两个子系统）。"""
import json
import os
import sys

from dedupapi import Stream


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "events.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    stream = Stream(spec["window"], spec["expected"])
    decisions = []
    for item in spec["events"]:
        decisions.append((item["id"], item["at"], stream.offer(item["id"], item["at"])["accepted"]))
    swept = stream.sweep(spec["sweep_at"])
    again = stream.offer(spec["expired_id"], spec["sweep_at"] + 1)["accepted"]
    stats = stream.dedup.stats()
    print("判定序列 =", [(item[0], item[1], item[2]) for item in decisions])
    print("接受数 =", stats.get("accepted"))
    print("重复数 =", stats.get("duplicates"))
    print("过期条数 =", swept.get("expired"))
    print("窗口内保留条数 =", swept.get("kept"))
    print("过期后重投是否接受 =", again)
    print("内存预算（窗口内条数上限） =", stats.get("window"))
    print("恢复的条数 =", stream.restore())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
