# MLX Optimizer Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a repo-local `mlx-optimizer` Codex plugin with Python-first MLX optimization skills, references, audit scripts, templates, tests, and validation evidence.

**Architecture:** This repo remains the source of truth, and the actual plugin root lives at `plugins/mlx-optimizer/` so the plugin folder and `.codex-plugin/plugin.json` name both equal `mlx-optimizer`. The plugin is progressive-disclosure: a small router skill dispatches to focused specialist skills, which then load only the reference files needed for the task. Scripts are dependency-light Python utilities that gather evidence and candidate findings without rewriting user code.

**Tech Stack:** Codex plugin manifest JSON, Codex skills as Markdown, Python 3 stdlib scripts, `unittest` smoke tests, MLX documentation references, plugin-creator validation scripts.

---

## File Structure

Create or modify these files:

- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/.gitignore`
  Ignores repo-local virtual environments, Python caches, test caches, generated reports, and macOS metadata.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/README.md`
  Explains plugin purpose, layout, validation, and local usage.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/.codex-plugin/plugin.json`
  Valid plugin manifest with concrete metadata and `skills` path.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-optimizer/SKILL.md`
  Entry-point router skill.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-performance-audit/SKILL.md`
  Repo audit workflow skill.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-training-optimizer/SKILL.md`
  Training-loop optimization workflow skill.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-inference-optimizer/SKILL.md`
  Inference-loop optimization workflow skill.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-metal-kernels/SKILL.md`
  Metal profiling, custom-kernel, and extension escalation skill.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-portability-bridges/SKILL.md`
  Swift/C/C++ and non-native-language bridge skill.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/mlx-core-concepts.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/eval-and-synchronization.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/compile-and-transforms.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/memory-and-dtypes.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/training-patterns.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/inference-patterns.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/profiling-and-metal.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/portability-bridges.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/reporting-format.md`
  Reference library used by the progressive skills.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/optimization-report.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/benchmark-notes.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/before-after-verification.md`
  Copy-ready report and verification templates.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_audit.py`
  Static MLX Python repo scanner.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_env_probe.py`
  Repo-local environment and MLX capability probe.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_benchmark_template.py`
  Copy-ready benchmark harness template.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/fixtures/mlx_project/train.py`
  Test fixture containing MLX performance smells.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/fixtures/plain_project/plain.py`
  Test fixture without MLX.
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/test_mlx_tools.py`
  `unittest` smoke tests for audit and environment-probe scripts.

## Task 1: Repo Hygiene And Plugin Scaffold

**Files:**
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/.gitignore`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/README.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/.codex-plugin/plugin.json`

- [ ] **Step 1: Confirm clean starting state**

Run:

```bash
/bin/zsh -lic 'git --no-pager status --short'
```

Expected: no output.

- [ ] **Step 2: Create repo hygiene files**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/.gitignore` with this content:

```gitignore
.DS_Store
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage
reports/
*.tmp
```

Create `/Users/andrew/Documents/mlx-optimizer-plugin/README.md` with this content:

````markdown
# MLX Optimizer Plugin

Repo-local Codex plugin for Python-first MLX optimization on Apple Silicon.

The plugin source lives in `plugins/mlx-optimizer/` so the plugin folder name
matches the manifest name. It provides progressive-disclosure skills, MLX
optimization references, stdlib-only audit scripts, benchmark templates, and
smoke tests.

## Layout

- `plugins/mlx-optimizer/.codex-plugin/plugin.json` is the plugin manifest.
- `plugins/mlx-optimizer/skills/` contains Codex skills.
- `plugins/mlx-optimizer/references/` contains task-routed MLX guidance.
- `plugins/mlx-optimizer/scripts/` contains local audit and probe tools.
- `plugins/mlx-optimizer/templates/` contains report templates.
- `tests/` contains stdlib `unittest` smoke tests.

## Local Validation

Use the repo-local virtual environment for Python commands:

```bash
python3 -m venv .venv
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py
python3 /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer
```

Do not install Python packages globally.
````

- [ ] **Step 3: Scaffold the plugin root**

Run the plugin-creator scaffold from its skill root:

```bash
/bin/zsh -lic 'cd /Users/andrew/.codex/skills/.system/plugin-creator && python3 scripts/create_basic_plugin.py mlx-optimizer --path /Users/andrew/Documents/mlx-optimizer-plugin/plugins --with-skills --with-scripts --with-assets'
```

Expected: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/.codex-plugin/plugin.json` exists.

- [ ] **Step 4: Replace scaffold manifest with final metadata**

Replace `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/.codex-plugin/plugin.json` with:

```json
{
  "name": "mlx-optimizer",
  "version": "0.1.0",
  "description": "Python-first MLX optimization skills, references, and audit scripts for Apple Silicon.",
  "author": {
    "name": "Andrew"
  },
  "license": "MIT",
  "keywords": [
    "mlx",
    "apple-silicon",
    "performance",
    "optimization",
    "python",
    "metal"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "MLX Optimizer",
    "shortDescription": "Audit and optimize Python MLX code on Apple Silicon.",
    "longDescription": "Python-first Codex skills, MLX references, audit scripts, benchmark templates, and verification workflows for optimizing MLX projects on Apple Silicon.",
    "developerName": "Andrew",
    "category": "Productivity",
    "capabilities": [
      "Interactive",
      "Write"
    ],
    "defaultPrompt": [
      "Audit this repo for MLX performance issues.",
      "Optimize this MLX training loop.",
      "Build an MLX benchmark plan."
    ],
    "brandColor": "#0F766E"
  }
}
```

- [ ] **Step 5: Validate manifest**

Run:

```bash
/bin/zsh -lic 'python3 /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer'
```

Expected: validation exits `0`.

- [ ] **Step 6: Commit scaffold**

Run:

```bash
/bin/zsh -lic 'git add .gitignore README.md plugins/mlx-optimizer/.codex-plugin/plugin.json && git diff --cached --check && git commit -m "chore: scaffold MLX optimizer plugin"'
```

Expected: commit succeeds.

## Task 2: Reference Library And Templates

**Files:**
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/references/*.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/*.md`

- [ ] **Step 1: Create reference and template directories**

Run:

```bash
/bin/zsh -lic 'mkdir -p plugins/mlx-optimizer/references plugins/mlx-optimizer/templates'
```

Expected: both directories exist.

- [ ] **Step 2: Create `references/mlx-core-concepts.md`**

Write:

```markdown
# MLX Core Concepts

Use this reference when reasoning about why MLX code behaves differently from
eager CPU/GPU frameworks.

## Optimization Facts

- MLX uses lazy evaluation. Array operations build a graph until evaluation is
  requested.
- MLX graphs are dynamic. Shape changes and Python control flow can affect
  compilation and benchmarking.
- MLX uses unified memory on Apple Silicon. CPU and GPU share memory, so copying
  costs differ from discrete-GPU systems, but synchronization still matters.
- MLX can execute on different devices and streams. Device/stream decisions
  should be measured on the target workload.

## Audit Questions

- Where is the first forced evaluation in the hot path?
- Is the graph allowed to grow too large before `mx.eval`?
- Are CPU reads, printing, or NumPy conversions forcing sync in loops?
- Is benchmark timing measuring scheduled work or completed work?
- Are model, optimizer, and data arrays using a consistent dtype policy?

## Evidence Required

Use timing, memory telemetry, representative inputs, and correctness checks.
Do not treat static observations as proven performance regressions.
```

- [ ] **Step 3: Create `references/eval-and-synchronization.md`**

Write:

````markdown
# Evaluation And Synchronization

Use this reference for `mx.eval`, `mx.async_eval`, `.item()`, printing, NumPy
conversion, and benchmark timing.

## Rules

- `mx.eval` is a synchronization boundary. Place it intentionally.
- `.item()`, `.tolist()`, NumPy conversion, and printing values can force CPU
  reads. Inside hot loops they often dominate runtime.
- A benchmark must warm up, run the workload, then force completion before
  stopping the timer.
- Too little evaluation can build large graphs and increase memory pressure.
- Too much evaluation can serialize work and hide MLX scheduling benefits.

## Suspicious Patterns

```python
for batch in batches:
    loss = step(batch)
    print(loss.item())
```

Prefer collecting periodic scalar metrics outside the hottest part of the loop:

```python
for step_index, batch in enumerate(batches):
    loss = step(batch)
    if step_index % log_every == 0:
        mx.eval(loss)
        print(float(loss.item()))
```

## Verification

Record before/after wall time, correctness result, active memory, peak memory,
cache memory when available, input shape, batch size, and MLX version.
````

- [ ] **Step 4: Create `references/compile-and-transforms.md`**

Write:

````markdown
# Compile And Transforms

Use this reference for `mx.compile`, `mx.grad`, `mx.value_and_grad`, `mx.vmap`,
and `mx.checkpoint`.

## Compile Fit

Good candidates:

- Pure numerical functions with stable argument structure.
- Repeated hot functions where compile overhead is amortized.
- Training steps that avoid host-side side effects.

Risky candidates:

- Functions that print, mutate global state, perform file I/O, or branch heavily
  on Python values.
- Functions whose shapes change constantly.
- Functions where one-off compile cost exceeds saved runtime.

## Training Transform Pattern

```python
def loss_fn(model, batch):
    logits = model(batch["x"])
    return cross_entropy(logits, batch["y"])

loss_and_grad = mx.value_and_grad(model, loss_fn)
loss, grads = loss_and_grad(model, batch)
optimizer.update(model, grads)
mx.eval(model.parameters(), optimizer.state, loss)
```

## Checkpointing

Use rematerialization when activation memory is the bottleneck and recomputation
is cheaper than storing intermediates. Verify with peak-memory and wall-time
measurements because checkpointing trades memory for compute.
````

- [ ] **Step 5: Create `references/memory-and-dtypes.md`**

Write:

```markdown
# Memory And Dtypes

Use this reference for MLX memory telemetry, cache behavior, dtype policy, and
OOM triage.

## Memory APIs To Check

- `mx.get_active_memory()`
- `mx.get_peak_memory()`
- `mx.get_cache_memory()`
- `mx.set_memory_limit(bytes)`
- `mx.set_cache_limit(bytes)`
- `mx.set_wired_limit(bytes)`
- `mx.clear_cache()`

## Dtype Policy

- Keep model parameters, activations, and optimizer state dtype choices explicit.
- BF16 is often a good training target on Apple Silicon when supported by the
  workload.
- FP16 can reduce memory but may need numerical checks.
- FP32 is safest for correctness baselines and sensitive reductions.

## OOM Triage Order

1. Reproduce with a small command and record input shape, batch size, dtype, and
   peak memory.
2. Reduce batch residency, prefetch depth, and validation batch size.
3. Remove avoidable graph growth by adding measured evaluation boundaries.
4. Test checkpointing on memory-heavy blocks.
5. Consider cache limits only after confirming graph and batch behavior.
```

- [ ] **Step 6: Create `references/training-patterns.md`**

Write:

````markdown
# Training Patterns

Use this reference for MLX training loops.

## Required Review Points

- `mx.value_and_grad` placement.
- Optimizer update path.
- Gradient accumulation semantics.
- Validation cadence and synchronization.
- Checkpoint write cadence.
- Dataloader worker, prefetch, and queue depth.
- Progress reporting with ETA for dataset/file loops.
- Memory telemetry at meaningful intervals.

## Verification Command Shape

Use one short smoke run and one representative benchmark run:

```bash
.venv/bin/python -m pytest tests/path/test_training.py -q
.venv/bin/python scripts/benchmark_training.py --steps 50 --batch-size 4
```

If the repo does not use pytest, run the repo's existing test command instead.
Report the exact command, exit code, and key output.
````

- [ ] **Step 7: Create `references/inference-patterns.md`**

Write:

```markdown
# Inference Patterns

Use this reference for MLX inference, generation, and serving loops.

## Review Points

- Warmup before timing.
- Batch size and prompt/input shape.
- KV-cache or recurrent-state growth.
- Quantized model loading and dtype consistency.
- Streaming output synchronization.
- Scalar extraction inside token or frame loops.
- Long-running memory growth and cache behavior.

## Benchmark Rules

- Time representative input sizes.
- Force completion before stopping the timer.
- Separate first-token or first-output latency from steady-state throughput.
- Record correctness or output-equivalence criteria.
- Report MLX version, hardware, Python executable, and memory telemetry.
```

- [ ] **Step 8: Create `references/profiling-and-metal.md`**

Write:

```markdown
# Profiling And Metal

Use this reference when normal MLX-level optimization is not enough.

## Escalation Order

1. Verify the workload is actually MLX/Metal-backed.
2. Fix obvious synchronization, dtype, batch, and graph-growth issues.
3. Measure active, peak, and cache memory.
4. Use MLX Metal capture APIs for GPU profiling.
5. Consider `mx.fast` primitives, custom Metal kernels, or C++ extensions only
   after profiling identifies a kernel-level bottleneck.

## Custom Kernel Gate

Recommend custom Metal kernels only when all are true:

- Built-in MLX operations cannot express the operation efficiently.
- Profiling shows the operation is a major runtime or memory bottleneck.
- Correctness tests exist for representative shapes and dtypes.
- The repo can maintain Metal code and native build tooling.
```

- [ ] **Step 9: Create `references/portability-bridges.md`**

Write:

```markdown
# Portability Bridges

Use this reference when MLX Python work needs to integrate with another
language or application runtime.

## Native MLX Surfaces

- Python is the v1 optimization focus for this plugin.
- Swift is the practical Apple-app integration path.
- C and C++ are native extension and lower-level integration paths.

## Other Languages

For Rust, Go, JavaScript, Java, Kotlin, and other ecosystems, prefer explicit
boundaries:

- Call a Python service or subprocess for MLX execution.
- Use a C ABI wrapper when a native boundary is required.
- Export to Core ML or another deployment format when MLX runtime access is not
  required.
- Keep data marshaling and synchronization costs in the benchmark.
```

- [ ] **Step 10: Create `references/reporting-format.md`**

Write:

```markdown
# Reporting Format

Every MLX optimization report must include these sections.

## Summary

One paragraph with target repo, target workload, and verdict.

## Findings

Each finding includes severity, file, line, evidence, candidate impact, and
confidence.

## Suggested Actions

List bounded edits or experiments. Avoid automatic rewrites without active
code-path evidence.

## Verification

Record commands, exit codes, timing, memory telemetry, correctness checks, MLX
version, Python executable, and hardware details.

## Residual Risks

State what was not measured, what may be workload-specific, and what should be
rechecked after larger input sizes or longer runs.
```

- [ ] **Step 11: Create templates**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/optimization-report.md`:

```markdown
# MLX Optimization Report

## Summary

- Target repo:
- Workload:
- Verdict:

## Findings

| Severity | File | Line | Evidence | Candidate impact | Confidence |
| --- | --- | ---: | --- | --- | --- |

## Suggested Actions

| Priority | Action | Verification |
| --- | --- | --- |

## Verification

- Baseline command:
- Baseline result:
- After command:
- After result:
- Correctness check:
- Memory telemetry:

## Residual Risks

- Residual risk entry.
```

Create `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/benchmark-notes.md`:

```markdown
# MLX Benchmark Notes

- Repo:
- Python executable:
- MLX version:
- Hardware:
- Input shape:
- Batch size:
- Warmup runs:
- Measured runs:
- Synchronization boundary:
- Median wall time:
- Peak memory:
- Correctness criterion:
```

Create `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/templates/before-after-verification.md`:

```markdown
# Before/After Verification

## Baseline

- Command:
- Exit code:
- Runtime:
- Active memory:
- Peak memory:
- Cache memory:
- Correctness:

## Change

- Files changed:
- Intended effect:

## After

- Command:
- Exit code:
- Runtime:
- Active memory:
- Peak memory:
- Cache memory:
- Correctness:

## Decision

- Keep change:
- Reason:
- Residual risk:
```

- [ ] **Step 12: Check references and templates**

Run:

```bash
/bin/zsh -lic 'python3 - <<'"'"'PY'"'"'
from pathlib import Path

patterns = [
    "T" + "BD",
    "TO" + "DO",
    "[" + "TO" + "DO",
    "PLACE" + "HOLDER",
    "FIX" + "ME",
    "X" * 3,
    "fill" + " in",
    "implement" + " later",
]
roots = [Path("plugins/mlx-optimizer/references"), Path("plugins/mlx-optimizer/templates")]
hits = []
for root in roots:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for number, line in enumerate(text.splitlines(), start=1):
                if any(pattern in line for pattern in patterns):
                    hits.append(f"{path}:{number}:{line}")
if hits:
    print("\n".join(hits))
    raise SystemExit(1)
PY'
```

Expected: no output.

- [ ] **Step 13: Commit reference library**

Run:

```bash
/bin/zsh -lic 'git add plugins/mlx-optimizer/references plugins/mlx-optimizer/templates && git diff --cached --check && git commit -m "docs: add MLX optimization references"'
```

Expected: commit succeeds.

## Task 3: Progressive-Disclosure Skills

**Files:**
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-optimizer/SKILL.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-performance-audit/SKILL.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-training-optimizer/SKILL.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-inference-optimizer/SKILL.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-metal-kernels/SKILL.md`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-portability-bridges/SKILL.md`

- [ ] **Step 1: Create router skill**

Write `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-optimizer/SKILL.md`:

```markdown
---
name: mlx-optimizer
description: Route Python-first MLX optimization work on Apple Silicon to focused audit, training, inference, Metal, or bridge workflows.
---

# MLX Optimizer

Use this skill when the user asks Codex to optimize, audit, benchmark, profile,
or explain MLX code on Apple Silicon.

## First Actions

1. Identify the target repo or file.
2. Check for a repo-local `.venv` before any Python execution.
3. Inspect project structure before proposing new modules.
4. Treat static observations as candidate findings until verified.
5. Require concrete evidence for optimization claims.

## Routing

- Repo-wide or unknown performance issue: read `../mlx-performance-audit/SKILL.md`.
- Training loop issue: read `../mlx-training-optimizer/SKILL.md`.
- Inference or generation issue: read `../mlx-inference-optimizer/SKILL.md`.
- Metal capture, custom kernel, or C++ extension question: read `../mlx-metal-kernels/SKILL.md`.
- Swift/C/C++ or other language integration: read `../mlx-portability-bridges/SKILL.md`.

## Core References

Read only the files needed for the routed task:

- `../../references/mlx-core-concepts.md`
- `../../references/eval-and-synchronization.md`
- `../../references/compile-and-transforms.md`
- `../../references/memory-and-dtypes.md`
- `../../references/reporting-format.md`

## Non-Negotiables

- Never install Python packages globally.
- Preserve unrelated user changes.
- Prefer existing repo abstractions.
- Do not recommend automatic rewrites without active code-path evidence.
- Include commands, outcomes, and residual risks in the final handoff.
```

- [ ] **Step 2: Create audit skill**

Write `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-performance-audit/SKILL.md`:

```markdown
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
```

- [ ] **Step 3: Create training skill**

Write `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-training-optimizer/SKILL.md`:

```markdown
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
2. Check how `mx.value_and_grad`, optimizer state, and `mx.eval` are used.
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
```

- [ ] **Step 4: Create inference skill**

Write `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-inference-optimizer/SKILL.md`:

```markdown
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
```

- [ ] **Step 5: Create Metal escalation skill**

Write `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-metal-kernels/SKILL.md`:

```markdown
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
```

- [ ] **Step 6: Create bridge skill**

Write `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/skills/mlx-portability-bridges/SKILL.md`:

```markdown
---
name: mlx-portability-bridges
description: Advise on Python-first MLX integration with Swift, C, C++, and non-native language boundaries.
---

# MLX Portability Bridges

Use this skill when the user asks how MLX work should cross language or app
runtime boundaries.

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
```

- [ ] **Step 7: Validate skills**

Run:

```bash
/bin/zsh -lic 'for skill in plugins/mlx-optimizer/skills/*; do python3 /Users/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"; done'
```

Expected: each skill validates.

- [ ] **Step 8: Commit skills**

Run:

```bash
/bin/zsh -lic 'git add plugins/mlx-optimizer/skills && git diff --cached --check && git commit -m "feat: add MLX optimization skills"'
```

Expected: commit succeeds.

## Task 4: Audit Script With Tests

**Files:**
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/fixtures/mlx_project/train.py`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/fixtures/plain_project/plain.py`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/test_mlx_tools.py`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_audit.py`

- [ ] **Step 1: Create fixture files**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/tests/fixtures/mlx_project/train.py`:

```python
import time

import mlx.core as mx


def train_epoch(batches):
    losses = []
    for batch in batches:
        loss = mx.sum(batch)
        print(loss.item())
        mx.eval(loss)
        losses.append(loss)
    return losses


def benchmark(batch):
    start = time.perf_counter()
    value = mx.sum(batch)
    end = time.perf_counter()
    return end - start, value
```

Create `/Users/andrew/Documents/mlx-optimizer-plugin/tests/fixtures/plain_project/plain.py`:

```python
def add(left, right):
    return left + right
```

- [ ] **Step 2: Write failing audit tests**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/tests/test_mlx_tools.py` with the audit tests:

```python
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
```

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest tests.test_mlx_tools.MlxAuditTests -v'
```

Expected: fails because `plugins/mlx-optimizer/scripts/mlx_audit.py` does not exist or has no implementation.

- [ ] **Step 3: Implement `mlx_audit.py`**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_audit.py`:

```python
#!/usr/bin/env python3
"""Static MLX Python audit tool.

The scanner reports candidate findings only. It never edits target code.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
}


@dataclass
class Finding:
    category: str
    severity: str
    file: str
    line: int
    evidence: str
    candidate_impact: str
    recommendation: str
    confidence: str


class Progress:
    def __init__(self, total: int) -> None:
        self.total = max(total, 1)
        self.start = time.monotonic()

    def update(self, count: int, label: str) -> None:
        elapsed = max(time.monotonic() - self.start, 0.001)
        rate = count / elapsed
        remaining = max(self.total - count, 0)
        eta = remaining / rate if rate else 0.0
        print(
            f"Scanning {count}/{self.total} files | ETA {eta:0.1f}s | {label}",
            file=sys.stderr,
        )


def iter_python_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".py":
        return [root]
    files: list[Path] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def is_mlx_import(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(alias.name == "mlx" or alias.name.startswith("mlx.") for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        return bool(node.module and (node.module == "mlx" or node.module.startswith("mlx.")))
    return False


def call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Attribute):
        parts = [func.attr]
        value = func.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if isinstance(value, ast.Name):
            parts.append(value.id)
        return ".".join(reversed(parts))
    if isinstance(func, ast.Name):
        return func.id
    return ""


class FileAnalyzer(ast.NodeVisitor):
    def __init__(self, path: Path, source: str, repo_root: Path) -> None:
        self.path = path
        self.source = source
        self.repo_root = repo_root
        self.findings: list[Finding] = []
        self.loop_depth = 0
        self.has_mlx_import = False
        self.has_timing_call = False
        self.has_eval_call = False

    @property
    def display_path(self) -> str:
        try:
            return str(self.path.relative_to(self.repo_root))
        except ValueError:
            return str(self.path)

    def add(self, category: str, severity: str, node: ast.AST, evidence: str, impact: str, recommendation: str, confidence: str) -> None:
        self.findings.append(
            Finding(
                category=category,
                severity=severity,
                file=self.display_path,
                line=getattr(node, "lineno", 1),
                evidence=evidence,
                candidate_impact=impact,
                recommendation=recommendation,
                confidence=confidence,
            )
        )

    def visit_Import(self, node: ast.Import) -> None:
        if is_mlx_import(node):
            self.has_mlx_import = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if is_mlx_import(node):
            self.has_mlx_import = True
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Call(self, node: ast.Call) -> None:
        name = call_name(node)
        if name.endswith("perf_counter") or name.endswith("timeit"):
            self.has_timing_call = True
        if name.endswith("mx.eval") or name == "eval":
            self.has_eval_call = True
            if self.loop_depth:
                self.add(
                    "eval-in-loop",
                    "medium",
                    node,
                    name,
                    "Repeated evaluation can serialize work and reduce MLX scheduling benefits.",
                    "Measure whether this evaluation boundary is needed on every iteration.",
                    "medium",
                )
        if self.loop_depth and any(name.endswith(suffix) for suffix in (".item", ".tolist", ".numpy")):
            self.add(
                "sync-in-loop",
                "high",
                node,
                name,
                "Scalar or host conversion inside a loop can force synchronization.",
                "Move scalar extraction to a lower-frequency logging path and benchmark before/after.",
                "high",
            )
        self.generic_visit(node)

    def finalize(self) -> None:
        if self.has_mlx_import and self.has_timing_call and not self.has_eval_call:
            synthetic = ast.parse("pass").body[0]
            synthetic.lineno = 1
            self.add(
                "benchmark-missing-eval",
                "medium",
                synthetic,
                "timing call without mx.eval in file",
                "Benchmark may time scheduled work instead of completed MLX work.",
                "Force completion before stopping timers and record the synchronization boundary.",
                "medium",
            )


def analyze_file(path: Path, root: Path) -> tuple[bool, list[Finding]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    analyzer = FileAnalyzer(path, source, root)
    analyzer.visit(tree)
    analyzer.finalize()
    return analyzer.has_mlx_import, analyzer.findings


def render_markdown(payload: dict) -> str:
    lines = [
        "# MLX Audit Report",
        "",
        "## Summary",
        "",
        f"- Target: `{payload['target']}`",
        f"- Files scanned: {payload['summary']['files_scanned']}",
        f"- Files with MLX imports: {payload['summary']['mlx_files']}",
        f"- Findings: {payload['summary']['finding_count']}",
        "",
        "## Findings",
        "",
    ]
    if not payload["findings"]:
        lines.append("No MLX candidate findings detected.")
    for finding in payload["findings"]:
        lines.extend(
            [
                f"### {finding['severity'].upper()} {finding['category']}",
                "",
                f"- File: `{finding['file']}:{finding['line']}`",
                f"- Evidence: `{finding['evidence']}`",
                f"- Candidate impact: {finding['candidate_impact']}",
                f"- Recommendation: {finding['recommendation']}",
                f"- Confidence: {finding['confidence']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Verification",
            "",
            "Run representative benchmarks with warmup, explicit completion, memory telemetry, and correctness checks.",
            "",
            "## Residual Risks",
            "",
            "Static scanning can miss dynamic MLX behavior and can report false positives. Verify against the live workload.",
            "",
        ]
    )
    return "\n".join(lines)


def build_payload(target: Path) -> dict:
    root = target.resolve()
    files = iter_python_files(root)
    progress = Progress(len(files))
    findings: list[Finding] = []
    mlx_files = 0
    for index, path in enumerate(files, start=1):
        progress.update(index, str(path))
        try:
            has_mlx, file_findings = analyze_file(path, root if root.is_dir() else root.parent)
        except SyntaxError as exc:
            findings.append(
                Finding(
                    category="syntax-error",
                    severity="low",
                    file=str(path),
                    line=exc.lineno or 1,
                    evidence=str(exc),
                    candidate_impact="File could not be scanned.",
                    recommendation="Fix syntax before relying on static audit output.",
                    confidence="high",
                )
            )
            continue
        if has_mlx:
            mlx_files += 1
            findings.extend(file_findings)
    return {
        "target": str(root),
        "summary": {
            "files_scanned": len(files),
            "mlx_files": mlx_files,
            "finding_count": len(findings),
        },
        "findings": [asdict(finding) for finding in findings],
    }


def write_output(payload: dict, output_format: str, output: Path | None) -> None:
    if output_format == "json":
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    else:
        text = render_markdown(payload)
    if output:
        output.write_text(text, encoding="utf-8")
    else:
        print(text)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Python MLX repos for candidate performance findings.")
    parser.add_argument("target", type=Path, help="Repo, directory, or Python file to scan.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Output file. Defaults to stdout.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if not args.target.exists():
        print(f"Target does not exist: {args.target}", file=sys.stderr)
        return 2
    payload = build_payload(args.target)
    write_output(payload, args.format, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run audit tests**

Run:

```bash
/bin/zsh -lic 'python3 -m venv .venv && .venv/bin/python -m unittest tests.test_mlx_tools.MlxAuditTests -v'
```

Expected: two audit tests pass.

- [ ] **Step 5: Check audit script syntax**

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/mlx_audit.py'
```

Expected: command exits `0`.

- [ ] **Step 6: Commit audit script**

Run:

```bash
/bin/zsh -lic 'git add tests/fixtures tests/test_mlx_tools.py plugins/mlx-optimizer/scripts/mlx_audit.py && git diff --cached --check && git commit -m "feat: add MLX static audit script"'
```

Expected: commit succeeds.

## Task 5: Environment Probe Script With Tests

**Files:**
- Modify: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/test_mlx_tools.py`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_env_probe.py`

- [ ] **Step 1: Add failing environment-probe tests**

Append these tests to `tests/test_mlx_tools.py`:

```python

class MlxEnvProbeTests(unittest.TestCase):
    def test_env_probe_reports_missing_venv(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(PLAIN_FIXTURE),
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "missing-venv")
        self.assertIn(".venv", payload["recommended_action"])

    def test_env_probe_uses_explicit_python(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ENV_PROBE),
                str(PLAIN_FIXTURE),
                "--python",
                sys.executable,
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(Path(payload["python"]["executable"]).resolve(), Path(sys.executable).resolve())
```

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest tests.test_mlx_tools.MlxEnvProbeTests -v'
```

Expected: fails because `mlx_env_probe.py` does not exist.

- [ ] **Step 2: Implement `mlx_env_probe.py`**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_env_probe.py`:

```python
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
```

- [ ] **Step 3: Run environment tests**

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest tests.test_mlx_tools.MlxEnvProbeTests -v'
```

Expected: two environment-probe tests pass.

- [ ] **Step 4: Run full tests and syntax checks**

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest discover -s tests -v && .venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/mlx_audit.py plugins/mlx-optimizer/scripts/mlx_env_probe.py'
```

Expected: all tests pass and syntax checks exit `0`.

- [ ] **Step 5: Commit environment probe**

Run:

```bash
/bin/zsh -lic 'git add tests/test_mlx_tools.py plugins/mlx-optimizer/scripts/mlx_env_probe.py && git diff --cached --check && git commit -m "feat: add MLX environment probe"'
```

Expected: commit succeeds.

## Task 6: Benchmark Template Script

**Files:**
- Modify: `/Users/andrew/Documents/mlx-optimizer-plugin/tests/test_mlx_tools.py`
- Create: `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_benchmark_template.py`

- [ ] **Step 1: Add benchmark-template smoke test**

Append this test to `tests/test_mlx_tools.py`:

```python

class MlxBenchmarkTemplateTests(unittest.TestCase):
    def test_benchmark_template_runs_without_mlx(self):
        script = ROOT / "plugins" / "mlx-optimizer" / "scripts" / "mlx_benchmark_template.py"
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--runs",
                "2",
                "--warmup",
                "1",
                "--format",
                "json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["runs"], 2)
        self.assertIn("median_seconds", payload)
        self.assertIn("Benchmark", result.stderr)
```

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest tests.test_mlx_tools.MlxBenchmarkTemplateTests -v'
```

Expected: fails because `mlx_benchmark_template.py` does not exist.

- [ ] **Step 2: Implement benchmark template**

Create `/Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer/scripts/mlx_benchmark_template.py`:

```python
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
```

- [ ] **Step 3: Run benchmark-template test**

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest tests.test_mlx_tools.MlxBenchmarkTemplateTests -v'
```

Expected: benchmark-template test passes.

- [ ] **Step 4: Run full script validation**

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest discover -s tests -v && .venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py'
```

Expected: all tests pass and all scripts compile.

- [ ] **Step 5: Commit benchmark template**

Run:

```bash
/bin/zsh -lic 'git add tests/test_mlx_tools.py plugins/mlx-optimizer/scripts/mlx_benchmark_template.py && git diff --cached --check && git commit -m "feat: add MLX benchmark template"'
```

Expected: commit succeeds.

## Task 7: Final Plugin Validation And Handoff Evidence

**Files:**
- Modify: `/Users/andrew/Documents/mlx-optimizer-plugin/README.md`

- [ ] **Step 1: Add validation notes to README**

Append this section to `/Users/andrew/Documents/mlx-optimizer-plugin/README.md`:

````markdown

## Validation Evidence

Before handing off implementation, run:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py
python3 /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer
for skill in plugins/mlx-optimizer/skills/*; do python3 /Users/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"; done
```

Record command outcomes in the final response.
````

- [ ] **Step 2: Run placeholder and consistency scan**

Run:

```bash
/bin/zsh -lic 'python3 - <<'"'"'PY'"'"'
from pathlib import Path

patterns = [
    "T" + "BD",
    "TO" + "DO",
    "[" + "TO" + "DO",
    "PLACE" + "HOLDER",
    "FIX" + "ME",
    "X" * 3,
    "fill" + " in",
    "implement" + " later",
    "Add " + "appropriate " + "error handling",
    "Write tests " + "for the above",
    "Similar " + "to Task",
]
ignored_parts = {".git", ".venv", "__pycache__"}
ignored_file = Path("docs/superpowers/plans/2026-06-12-mlx-optimizer-plugin.md")
hits = []
for path in sorted(Path(".").rglob("*")):
    if not path.is_file():
        continue
    if path == ignored_file or any(part in ignored_parts for part in path.parts):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for number, line in enumerate(text.splitlines(), start=1):
        if any(pattern in line for pattern in patterns):
            hits.append(f"{path}:{number}:{line}")
if hits:
    print("\n".join(hits))
    raise SystemExit(1)
PY'
```

Expected: no output.

- [ ] **Step 3: Run full validation suite**

Run:

```bash
/bin/zsh -lic '.venv/bin/python -m unittest discover -s tests -v && .venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py && python3 /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer && for skill in plugins/mlx-optimizer/skills/*; do python3 /Users/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"; done'
```

Expected: all commands exit `0`.

- [ ] **Step 4: Inspect git state and staged diff**

Run:

```bash
/bin/zsh -lic 'git --no-pager status --short && git --no-pager diff --stat'
```

Expected: only intended final README change remains.

- [ ] **Step 5: Commit final validation docs**

Run:

```bash
/bin/zsh -lic 'git add README.md && git diff --cached --check && git commit -m "docs: document MLX plugin validation"'
```

Expected: commit succeeds.

- [ ] **Step 6: Final handoff check**

Run:

```bash
/bin/zsh -lic 'git --no-pager status --short && git --no-pager log --oneline -6'
```

Expected: working tree is clean, and recent commits show scaffold, references, skills, scripts, and validation docs.

## Self-Review Checklist

- Spec coverage:
  - Plugin scaffold and manifest: Task 1.
  - Progressive-disclosure skills: Task 3.
  - Reference library: Task 2.
  - Audit script with progress and json/markdown output: Task 4.
  - Environment probe respecting `.venv`: Task 5.
  - Benchmark template with warmup, synchronization, memory hook, and progress: Task 6.
  - Templates: Task 2.
  - Validation and smoke tests: Tasks 4 through 7.
  - Frequent Conventional Commits: every task ends with a commit step.
- Placeholder scan command: Task 7 Step 2.
- Type consistency:
  - Tests reference `AUDIT`, `ENV_PROBE`, `MLX_FIXTURE`, and `PLAIN_FIXTURE` defined in Task 4.
  - Script names match manifest-independent file paths under `plugins/mlx-optimizer/scripts/`.
  - Test class names are unique and discoverable by `unittest`.
- Residual implementation risk:
  - Static audit findings are intentionally conservative candidate findings.
  - Skill validator command may reveal stricter local formatting rules; fix validator-reported formatting directly in the affected `SKILL.md` file and rerun the same command.
