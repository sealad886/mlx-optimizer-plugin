---
name: mlx-portability-bridges
description: Advise on Python-first MLX integration with Swift, C, C++, and non-native language boundaries.
---

# MLX Portability Bridges

Use this skill when the user asks how MLX work should cross language or app
runtime boundaries.

## Python Environment

Before any Python execution, use the target repo's `.venv`. Never install
Python packages globally.

## Required References

- `../../references/portability-bridges.md`
- `../../references/profiling-and-metal.md`

## Workflow

1. Identify whether the target needs native MLX execution, app integration,
   service integration, or exported model deployment.
2. Prefer MLX Python for optimization work in v1.
3. Use MLX Swift for Apple app integration when runtime MLX execution is needed.
4. Use C/C++ for extension or low-level integration boundaries.
5. For other languages, recommend subprocess, service, C ABI, or Core ML/export
   boundaries, then include data marshaling costs in benchmarks.

## Boundary Rule

Do not claim equal-depth MLX optimization support for languages without a
first-class MLX API.
