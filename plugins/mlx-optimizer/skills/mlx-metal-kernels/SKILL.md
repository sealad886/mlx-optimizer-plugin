---
name: mlx-metal-kernels
description: Guide MLX Metal profiling, mx.fast escalation, custom Metal kernels, and C++ extensions when profiling proves kernel-level bottlenecks.
---

# MLX Metal Kernels

Use this skill only after normal MLX-level issues have been checked or when the
user explicitly asks about Metal capture, custom kernels, or native extensions.

## Required References

- `../../references/profiling-and-metal.md`
- `../../references/memory-and-dtypes.md`
- `../../references/compile-and-transforms.md`

## Workflow

1. Confirm MLX can see Metal and the workload is GPU-backed.
2. Check synchronization, dtype, batch, graph-growth, and memory issues first.
3. Ask for or collect profiling evidence.
4. Recommend `mx.fast`, custom Metal kernels, or C++ extensions only when the
   operation is a measured bottleneck and built-in MLX ops are insufficient.
5. Require correctness tests for representative shapes and dtypes.

## Final Handoff

State whether custom native work is justified, which evidence supports that
decision, and what maintenance burden it creates.
