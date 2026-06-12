#!/usr/bin/env python3
"""Probe a repo-local Python/MLX environment without global installs."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def default_venv_python(target: Path) -> Path:
    return target / ".venv" / "bin" / "python"


def child_probe() -> dict:
    payload: dict = {
        "python": {
            "executable": sys.executable,
            "version": sys.version.split()[0],
            "machine": platform.machine(),
            "platform": platform.platform(),
        },
        "mlx": {
            "available": False,
            "version": None,
            "metal_available": None,
            "device_info": None,
            "memory_api": {},
        },
    }
    try:
        import mlx.core as mx  # type: ignore
    except Exception as exc:
        payload["mlx"]["import_error"] = repr(exc)
        return payload

    payload["mlx"]["available"] = True
    payload["mlx"]["version"] = getattr(mx, "__version__", None)
    metal = getattr(mx, "metal", None)
    if metal is not None:
        is_available = getattr(metal, "is_available", None)
        device_info = getattr(metal, "device_info", None)
        payload["mlx"]["metal_available"] = bool(is_available()) if callable(is_available) else None
        payload["mlx"]["device_info"] = device_info() if callable(device_info) else None
    for name in (
        "get_active_memory",
        "get_peak_memory",
        "get_cache_memory",
        "set_memory_limit",
        "set_cache_limit",
        "set_wired_limit",
        "clear_cache",
    ):
        payload["mlx"]["memory_api"][name] = hasattr(mx, name)
    return payload


def run_child(python_executable: Path) -> dict:
    code = (
        "import json, runpy; "
        f"module = runpy.run_path({str(Path(__file__).resolve())!r}); "
        "print(json.dumps(module['child_probe'](), sort_keys=True))"
    )
    result = subprocess.run(
        [str(python_executable), "-c", code],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return {
            "status": "probe-failed",
            "python": {"executable": str(python_executable)},
            "stderr": result.stderr,
            "recommended_action": "Verify the repo-local Python executable can run basic Python code.",
        }
    payload = json.loads(result.stdout)
    payload["status"] = "ok"
    if not payload["mlx"]["available"]:
        payload["recommended_action"] = "Install MLX only inside the target repo .venv if the project requires MLX."
    return payload


def render_markdown(payload: dict) -> str:
    lines = ["# MLX Environment Probe", ""]
    lines.append(f"- Status: {payload['status']}")
    if "python" in payload:
        lines.append(f"- Python: `{payload['python'].get('executable')}`")
        lines.append(f"- Machine: `{payload['python'].get('machine')}`")
    if "mlx" in payload:
        lines.append(f"- MLX available: {payload['mlx'].get('available')}")
        lines.append(f"- MLX version: {payload['mlx'].get('version')}")
        lines.append(f"- Metal available: {payload['mlx'].get('metal_available')}")
    if "recommended_action" in payload:
        lines.append(f"- Recommended action: {payload['recommended_action']}")
    return "\n".join(lines) + "\n"


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe a repo-local Python/MLX environment.")
    parser.add_argument("target", type=Path, help="Target repo path.")
    parser.add_argument("--python", type=Path, help="Explicit Python executable.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    target = args.target.resolve()
    python_executable = args.python.resolve() if args.python else default_venv_python(target)
    if not args.python and not python_executable.exists():
        payload = {
            "status": "missing-venv",
            "target": str(target),
            "recommended_action": f"Create and use a repo-local virtual environment at {target / '.venv'}. Do not install Python packages globally.",
        }
    else:
        payload = run_child(python_executable)
        payload["target"] = str(target)
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
