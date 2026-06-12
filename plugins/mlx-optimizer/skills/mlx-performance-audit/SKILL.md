---
name: mlx-performance-audit
description: Audit Python MLX repos for lazy-eval, synchronization, compile, dtype, memory, progress, and benchmark issues.
---

# MLX Performance Audit

Use this skill for repo-wide MLX performance reviews and unknown bottlenecks.

## Required References

- `../../references/mlx-core-concepts.md`
- `../../references/eval-and-synchronization.md`
- `../../references/compile-and-transforms.md`
- `../../references/memory-and-dtypes.md`
- `../../references/reporting-format.md`

## Workflow

1. Inspect repo state with `git --no-pager status --short`.
2. Locate dependency files, MLX imports, training loops, inference loops,
   dataloaders, benchmark scripts, and progress-reporting patterns.
3. Run `plugins/mlx-optimizer/scripts/mlx_audit.py` from this plugin repo when
   the target repo is local and scanning is useful.
4. Keep candidate findings separate from verified findings.
5. Recommend measurement before changes: warmup, synchronization, repeated runs,
   memory telemetry, correctness checks, and representative input sizes.

## Report Shape

Use `../../templates/optimization-report.md` as the report structure. Every
finding needs file, line, evidence, candidate impact, confidence, verification,
and residual risk.
