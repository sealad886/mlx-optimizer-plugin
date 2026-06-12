#!/usr/bin/env python3
"""Copy-ready MLX benchmark harness template.

Replace workload() with the target MLX operation when copying this into a repo.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Iterable


def workload(size: int) -> int:
    total = 0
    for value in range(size):
        total += value * value
    return total


def synchronize() -> None:
    try:
        import mlx.core as mx  # type: ignore
    except Exception:
        return
    mx.eval(mx.array([0]))


def memory_snapshot() -> dict:
    try:
        import mlx.core as mx  # type: ignore
    except Exception:
        return {"mlx_available": False}
    snapshot = {"mlx_available": True}
    for key, name in (
        ("active", "get_active_memory"),
        ("peak", "get_peak_memory"),
        ("cache", "get_cache_memory"),
    ):
        func = getattr(mx, name, None)
        snapshot[key] = func() if callable(func) else None
    return snapshot


def progress(index: int, total: int, started: float) -> None:
    elapsed = max(time.monotonic() - started, 0.001)
    rate = index / elapsed
    eta = (total - index) / rate if rate else 0.0
    print(f"Benchmark {index}/{total} | ETA {eta:0.1f}s", file=sys.stderr)


def run_benchmark(runs: int, warmup: int, size: int) -> dict:
    for _ in range(warmup):
        workload(size)
        synchronize()
    durations: list[float] = []
    started = time.monotonic()
    for index in range(1, runs + 1):
        progress(index, runs, started)
        before = time.perf_counter()
        result = workload(size)
        synchronize()
        after = time.perf_counter()
        if result != sum(value * value for value in range(size)):
            raise RuntimeError("Correctness check failed for template workload.")
        durations.append(after - before)
    return {
        "runs": runs,
        "warmup": warmup,
        "size": size,
        "median_seconds": statistics.median(durations),
        "min_seconds": min(durations),
        "max_seconds": max(durations),
        "memory": memory_snapshot(),
    }


def render_markdown(payload: dict) -> str:
    return "\n".join(
        [
            "# MLX Benchmark Result",
            "",
            f"- Runs: {payload['runs']}",
            f"- Warmup: {payload['warmup']}",
            f"- Median seconds: {payload['median_seconds']:.6f}",
            f"- Min seconds: {payload['min_seconds']:.6f}",
            f"- Max seconds: {payload['max_seconds']:.6f}",
            f"- Memory: `{payload['memory']}`",
            "",
        ]
    )


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark harness template with warmup and synchronization.")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--size", type=int, default=10000)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    payload = run_benchmark(args.runs, args.warmup, args.size)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n" if args.format == "json" else render_markdown(payload)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
