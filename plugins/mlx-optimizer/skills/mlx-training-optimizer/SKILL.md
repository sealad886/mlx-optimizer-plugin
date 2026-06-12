---
name: mlx-training-optimizer
description: Optimize Python MLX training loops with value_and_grad, accumulation, checkpointing, dtype, validation cadence, memory telemetry, and progress reporting.
---

# MLX Training Optimizer

Use this skill when the user points to MLX model training, fine-tuning,
pretraining, loss computation, optimizer updates, or validation throughput.

## Required References

- `../../references/training-patterns.md`
- `../../references/eval-and-synchronization.md`
- `../../references/compile-and-transforms.md`
- `../../references/memory-and-dtypes.md`

## Workflow

1. Identify the exact training entry point and the hot step function.
2. Check the `value_and_grad` namespace and placement, optimizer state, and
   `mx.eval` usage.
3. Inspect gradient accumulation, checkpointing, validation cadence, data
   loading, prefetching, dtype casts, and scalar logging.
4. If code loops over files or folders, require progress output with ETA.
5. Propose changes only after the baseline command and correctness signal are
   known.
6. Verify with a short smoke run and a representative benchmark run.

## Evidence To Capture

- Command and exit code.
- Steps per second or wall time.
- Active, peak, and cache memory where available.
- Input shape, batch size, dtype policy, and MLX version.
- Correctness signal and residual risk.
