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
    def write_python(self, path, lines, encoding="utf-8"):
        path.write_text("\n".join(lines) + "\n", encoding=encoding)

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

    def run_audit_stdout_json(self, target):
        result = subprocess.run(
            [
                sys.executable,
                str(AUDIT),
                str(target),
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Scanning", result.stderr)
        return json.loads(result.stdout)

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
            self.write_python(
                target,
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
                ],
            )

            payload = self.run_audit_json(target)

        findings = [
            finding
            for finding in payload["findings"]
            if finding["category"] == "benchmark-missing-eval"
        ]
        self.assertEqual(len(findings), 1)

    def test_audit_recognizes_full_mlx_core_eval_in_timed_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "full_import.py"
            self.write_python(
                target,
                [
                    "import time",
                    "",
                    "import mlx.core",
                    "",
                    "",
                    "def benchmark(batches):",
                    "    start = time.perf_counter()",
                    "    for batch in batches:",
                    "        loss = mlx.core.sum(batch)",
                    "        mlx.core.eval(loss)",
                    "    end = time.perf_counter()",
                    "    return end - start",
                ],
            )

            payload = self.run_audit_json(target)

        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("eval-in-loop", categories)
        self.assertNotIn("benchmark-missing-eval", categories)

    def test_audit_recognizes_imported_eval_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "alias_eval.py"
            self.write_python(
                target,
                [
                    "import mlx.core as mx",
                    "from mlx.core import eval as mlx_eval",
                    "",
                    "",
                    "def train_epoch(batches):",
                    "    for batch in batches:",
                    "        loss = mx.sum(batch)",
                    "        mlx_eval(loss)",
                ],
            )

            payload = self.run_audit_json(target)

        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("eval-in-loop", categories)

    def test_audit_reads_python_source_encoding_cookie(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "latin1_bench.py"
            self.write_python(
                target,
                [
                    "# -*- coding: latin-1 -*-",
                    "# cafe: café",
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
                ],
                encoding="latin-1",
            )

            payload = self.run_audit_json(target)

        categories = {finding["category"] for finding in payload["findings"]}
        self.assertIn("benchmark-missing-eval", categories)

    def test_audit_writes_json_to_stdout_without_output(self):
        payload = self.run_audit_stdout_json(PLAIN_FIXTURE)

        self.assertEqual(payload["summary"]["files_scanned"], 1)
        self.assertEqual(payload["findings"], [])
