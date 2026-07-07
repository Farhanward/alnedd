from __future__ import annotations

import json
import statistics
import time
import tracemalloc
from pathlib import Path

from .core import work_order


def _p(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round((pct / 100) * (len(ordered) - 1))))]


def evaluate(path: str | Path, *, repeat: int = 1) -> dict:
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    owners: dict[str, int] = {}
    errors = 0
    latencies = []
    started = time.perf_counter()
    tracemalloc.start()
    for _ in range(repeat):
        for row in rows:
            t0 = time.perf_counter()
            try:
                order = work_order(str(row.get("message") or ""))
                owners[order["owner"]] = owners.get(order["owner"], 0) + 1
            except Exception:
                errors += 1
            latencies.append((time.perf_counter() - t0) * 1000)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"processed": len(rows) * repeat, "errors": errors, "owners": owners, "latency_ms": {"mean": statistics.fmean(latencies) if latencies else 0.0, "p99": _p(latencies, 99)}, "memory_mb": {"current": current / 1_000_000, "peak": peak / 1_000_000}, "elapsed_seconds": time.perf_counter() - started, "collapse_check": {"passed": errors == 0, "criteria": "errors == 0"}}

