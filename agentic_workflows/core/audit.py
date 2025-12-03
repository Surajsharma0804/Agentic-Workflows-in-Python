import json
from datetime import datetime, UTC
from pathlib import Path

class AuditLog:
    def __init__(self, path="audit.log"):
        self.path = Path(path)

    def record(self, entry: dict):
        entry = dict(entry)
        entry.setdefault("ts", datetime.now(UTC).isoformat())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
