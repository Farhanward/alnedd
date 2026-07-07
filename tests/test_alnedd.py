from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from alnedd.batch import evaluate
from alnedd.core import dashboard, init_registry, work_order
from alnedd.datasets import convert_bitext


class AlNeddTests(unittest.TestCase):
    def test_dashboard_and_order(self):
        with tempfile.TemporaryDirectory(dir="C:/Projects") as tmp:
            reg = Path(tmp) / "modules.json"
            init_registry(reg)
            self.assertIn(dashboard(reg)["status"], {"READY", "DEGRADED"})
            self.assertEqual(work_order("refund please")["owner"], "almandoub")

    def test_convert_and_batch_fixture(self):
        with tempfile.TemporaryDirectory(dir="C:/Projects") as tmp:
            src = Path(tmp) / "bitext.jsonl"
            out = Path(tmp) / "orders.jsonl"
            src.write_text('{"instruction":"refund please","intent":"refund"}\n', encoding="utf-8")
            convert_bitext(src, out)
            summary = evaluate(out)
            self.assertEqual(summary["errors"], 0)


if __name__ == "__main__":
    unittest.main()

