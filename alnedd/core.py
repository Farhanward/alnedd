from __future__ import annotations

import json
from pathlib import Path


DEFAULT_MODULES = [
    {"name": "almandoub", "path": "C:/Projects/almandoub", "role": "customer_messages"},
    {"name": "alkhaliya", "path": "C:/Projects/alkhaliya", "role": "automation"},
    {"name": "almasna_altaswiqi", "path": "C:/Projects/almasna_altaswiqi", "role": "marketing"},
    {"name": "alharis_alsahabi", "path": "C:/Projects/alharis_alsahabi", "role": "sre"},
]


def init_registry(path: str | Path) -> dict:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(DEFAULT_MODULES, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"out": str(out.resolve()), "modules": len(DEFAULT_MODULES)}


def load_registry(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        init_registry(p)
    return json.loads(p.read_text(encoding="utf-8"))


def dashboard(path: str | Path) -> dict:
    modules = load_registry(path)
    rows = []
    for module in modules:
        exists = Path(module["path"]).exists()
        rows.append({**module, "exists": exists, "status": "READY" if exists else "MISSING"})
    ready = sum(1 for row in rows if row["exists"])
    return {"modules": rows, "ready": ready, "total": len(rows), "status": "READY" if ready == len(rows) else "DEGRADED"}


def work_order(message: str) -> dict:
    low = message.casefold()
    if any(word in low for word in ("refund", "cancel", "support", "angry")):
        owner = "almandoub"
        kind = "customer_support"
    elif any(word in low for word in ("post", "marketing", "seo", "content")):
        owner = "almasna_altaswiqi"
        kind = "marketing"
    elif any(word in low for word in ("incident", "down", "error", "latency")):
        owner = "alharis_alsahabi"
        kind = "sre"
    else:
        owner = "alkhaliya"
        kind = "automation"
    return {"kind": kind, "owner": owner, "title": message[:100], "status": "TODO"}

