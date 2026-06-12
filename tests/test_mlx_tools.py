import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_audit.py"
ENV_PROBE = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_env_probe.py"
MLX_FIXTURE = ROOT / "tests" / "fixtures" / "mlx_project"
PLAIN_FIXTURE = ROOT / "tests" / "fixtures" / "plain_project"


class MlxAuditTests(unittest.TestCase):
    def run_audit_json(self, target):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "audit.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(AUDIT),
                    str(target),
                    "--format",
                    "json",
                    "--output",
                    str(output),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Scanning", result.stderr)
            return json.loads(output.read_text())

    def test_audit_reports_sync_and_eval_findings(self):
        payload = self.run_audit_json(MLX_FIXTURE)
        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("sync-in-loop", categories)
        self.assertIn("eval-in-loop", categories)
        self.assertIn("benchmark-missing-eval", categories)

    def test_audit_plain_project_has_no_mlx_findings(self):
        payload = self.run_audit_json(PLAIN_FIXTURE)
        self.assertEqual(payload["summary"]["files_scanned"], 1)
        self.assertEqual(payload["findings"], [])

    def test_audit_reports_single_missing_eval_per_timed_function(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "bench.py"
            target.write_text(
                "\n".join(
                    [
                        "import time",
                        "",
                        "import mlx.core as mx",
                        "",
                        "",
                        "def benchmark(batch):",
                        "    start = time.perf_counter()",
                        "    value = mx.sum(batch)",
                        "    end = time.perf_counter()",
                        "    return end - start, value",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            payload = self.run_audit_json(target)

        findings = [
            finding
            for finding in payload["findings"]
            if finding["category"] == "benchmark-missing-eval"
        ]
        self.assertEqual(len(findings), 1)
