---
name: mlx-inference-optimizer
description: Optimize Python MLX inference and generation loops with warmup, batching, cache handling, synchronization, quantization, and memory checks.
---

# MLX Inference Optimizer

Use this skill for MLX inference, generation, serving loops, batch scoring,
streaming output, or latency/throughput questions.

## Required References

- `../../references/inference-patterns.md`
- `../../references/eval-and-synchronization.md`
- `../../references/memory-and-dtypes.md`

## Workflow

1. Identify the exact inference entry point and representative inputs.
2. Separate first-output latency from steady-state throughput.
3. Inspect warmup, batching, scalar extraction, streaming sync, cache growth,
   quantized model loading, and dtype policy.
4. Confirm the benchmark forces completion before stopping timers.
5. Verify output correctness or equivalence before accepting speedups.

## Evidence To Capture

- Prompt/input shape and batch size.
- Warmup and measured run counts.
- Synchronization boundary.
- Median and range of wall time.
- Memory telemetry.
- Correctness or output-equivalence rule.
