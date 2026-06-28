import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fsc_benchmark.io import load_jsonl, validate_jsonl

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "generations" / "demo_generations.jsonl"


class IoCliTests(unittest.TestCase):
    def test_load_example(self):
        records = load_jsonl(EXAMPLE)
        self.assertGreaterEqual(len(records), 1)

    def test_validate_example(self):
        ok, errors = validate_jsonl(EXAMPLE)
        self.assertTrue(ok, errors)

    def test_cli_taxonomy(self):
        proc = subprocess.run(
            [sys.executable, "-m", "fsc_benchmark.cli", "taxonomy"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("False Security Confidence", proc.stdout)

    def test_cli_metrics_json(self):
        proc = subprocess.run(
            [sys.executable, "-m", "fsc_benchmark.cli", "metrics", str(EXAMPLE), "--format", "json"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertIn("fsc_rate", data)


if __name__ == "__main__":
    unittest.main()
