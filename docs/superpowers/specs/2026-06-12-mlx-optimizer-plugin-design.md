# MLX Optimizer Plugin Design

Date: 2026-06-12
Status: approved for specification
Repo: `/Users/andrew/Documents/mlx-optimizer-plugin`

## Purpose

Create a repo-local Codex plugin named `mlx-optimizer` that helps Codex act like
an expert MLX-on-Apple-Silicon optimization partner. The first version is
Python-first. It provides deep MLX Python guidance, static audit scripts, and
benchmark/report templates, with supporting bridge guidance for Swift, C, and
C++ where those ecosystems affect Python MLX workflows.

The plugin must optimize through evidence, not assertion. It should help Codex
inspect the target repo, identify likely MLX performance and correctness risks,
recommend bounded changes, and require before/after validation with tests,
benchmarks, memory telemetry, and residual-risk notes.

## Scope

In scope for v1:

- Progressive-disclosure Codex skills for MLX optimization work.
- Python MLX performance, training, inference, benchmarking, memory, dtype, and
  Metal profiling guidance.
- Static audit scripts that scan Python repos and emit markdown/json findings.
- Environment probing that respects repo-local virtual environments.
- Benchmark and report templates.
- Supporting Swift/C/C++ and bridge guidance, not equal-depth optimization
  coverage for every language.
- Plugin validation, skill validation where applicable, script syntax checks,
  and smoke tests against a small fixture repo.

Out of scope for v1:

- Automatic code rewrites without repo-specific verification.
- A Codex MCP server. MCP tools are a future extension after script heuristics
  are proven useful.
- Equal-depth Rust, Go, JavaScript, Java, Kotlin, or other language support.
- Global Python package installation.
- Publishing to a non-default marketplace unless requested later.

## Research Basis

The design is grounded in current authoritative MLX documentation and plugin
manifest guidance:

- MLX is an array framework for Apple silicon with Python, C++, C, and Swift
  APIs, lazy computation, dynamic graphs, multi-device execution, and unified
  memory.
- MLX optimization must account for lazy evaluation. Computation is recorded
  until evaluation, and graph size versus evaluation frequency is a key tradeoff.
- `mx.compile`, `mx.checkpoint`, `mx.grad`, `mx.value_and_grad`, and `mx.vmap`
  are central optimization and training-loop tools.
- MLX exposes memory and cache APIs including active, peak, and cache memory
  telemetry, memory limits, cache limits, wired limits, and cache clearing.
- MLX exposes Metal availability/device info and Metal capture APIs for deeper
  profiling.
- Custom Metal kernels and C++ extensions are advanced escalation paths, not
  first-line optimization tactics.
- Codex plugin manifests require `.codex-plugin/plugin.json` with valid semver,
  concrete metadata, valid relative paths, and no placeholder values.

Primary sources used during design:

- https://github.com/ml-explore/mlx
- https://ml-explore.github.io/mlx/build/html/usage/lazy_evaluation.html
- https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html
- https://ml-explore.github.io/mlx/build/html/usage/compile.html
- https://ml-explore.github.io/mlx/build/html/python/transforms.html
- https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.set_memory_limit.html
- https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.set_cache_limit.html
- https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.set_wired_limit.html
- https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.clear_cache.html
- https://ml-explore.github.io/mlx/build/html/python/metal.html
- https://ml-explore.github.io/mlx/build/html/dev/metal_debugger.html
- https://ml-explore.github.io/mlx/build/html/dev/custom_metal_kernels.html
- https://ml-explore.github.io/mlx/build/html/dev/extensions.html
- https://github.com/ml-explore/mlx-swift
- `/Users/andrew/.codex/skills/.system/plugin-creator/references/plugin-json-spec.md`
- `/Users/andrew/.codex/skills/.system/plugin-creator/references/installing-and-updating.md`

## Architecture

V1 will be a repo-local plugin named `mlx-optimizer`, authored directly in this
repo. It will have four layers.

### Router Skill

`skills/mlx-optimizer/SKILL.md` is the entry point. It decides whether the user
needs a general audit, training-loop optimization, inference optimization,
Metal/custom-kernel escalation, portability/bridge guidance, or current-doc
research. It remains small and routes to deeper skills and reference files.

### Specialist Skills

Specialist skills each own one optimization mode:

- `skills/mlx-performance-audit/SKILL.md`
- `skills/mlx-training-optimizer/SKILL.md`
- `skills/mlx-inference-optimizer/SKILL.md`
- `skills/mlx-metal-kernels/SKILL.md`
- `skills/mlx-portability-bridges/SKILL.md`

Each specialist skill names the minimum reference files needed for that task so
Codex can use progressive disclosure instead of loading the whole plugin.

### Reference Library

`references/` contains compact, task-routed MLX guidance. The references explain
how to reason about MLX performance surfaces and how to verify claims with repo
evidence.

### Executable Scripts

`scripts/` contains conservative Python utilities. They gather evidence and
candidate findings, but do not rewrite user code. Any loop over folders or files
must report progress to a user-visible stream and include ETA where practical.

## Skill Hierarchy

### `mlx-optimizer`

Entry-point router. Responsibilities:

- Identify the requested task type.
- Ask only for missing context that cannot be discovered safely.
- Enforce repo-local `.venv` behavior for Python work.
- Route to the correct specialist skill and references.
- Require concrete verification evidence for optimization claims.

### `mlx-performance-audit`

General repo audit for MLX Python projects. Responsibilities:

- Discover MLX imports, dependency files, model code, training loops, inference
  loops, dataloaders, and benchmark scripts.
- Run or recommend `scripts/mlx_audit.py` where appropriate.
- Treat static findings as candidate findings until verified.
- Produce a report with findings, evidence, suggested edits, verification, and
  residual risks.

### `mlx-training-optimizer`

Training-loop specialist. Responsibilities:

- Analyze `mx.value_and_grad`, optimizer updates, gradient accumulation,
  checkpointing/rematerialization, validation cadence, dtype policy, dataloader
  pressure, and memory telemetry.
- Require correctness checks plus before/after timing and memory evidence.
- Preserve existing project abstractions before proposing new helpers.

### `mlx-inference-optimizer`

Inference specialist. Responsibilities:

- Analyze warmup, batching, generation loops, cache behavior, quantization,
  streaming synchronization, timing boundaries, and long-running process memory.
- Watch for `.item()`, printing, NumPy conversion, and excessive `mx.eval` in
  hot loops.
- Require representative prompts/inputs and correctness checks.

### `mlx-metal-kernels`

Advanced escalation specialist. Responsibilities:

- Decide whether built-in MLX ops, `mx.fast` primitives, custom Metal kernels,
  or C++ extensions are appropriate.
- Require profiling evidence before recommending custom kernels.
- Guide Metal capture workflows with `mx.metal.start_capture` and Xcode.

### `mlx-portability-bridges`

Bridge specialist. Responsibilities:

- Explain practical integration paths for Swift, C, and C++.
- For other languages, recommend C ABI, subprocess/service, exported-function,
  Core ML, or app-boundary approaches where appropriate.
- Avoid claiming native equal-depth MLX optimization support for languages that
  do not have first-class MLX APIs.

## References

Create the following reference files:

- `references/mlx-core-concepts.md`
  Lazy evaluation, dynamic graphs, unified memory, devices/streams, and why MLX
  optimization differs from PyTorch/JAX habits.

- `references/eval-and-synchronization.md`
  `mx.eval`, `mx.async_eval`, `.item()`, printing, NumPy conversion, benchmark
  timing boundaries, and graph-size tradeoffs.

- `references/compile-and-transforms.md`
  `mx.compile`, shapeless compilation, `grad`, `value_and_grad`, `vmap`,
  `checkpoint`, pure-function requirements, and compile-hostile patterns.

- `references/memory-and-dtypes.md`
  Active/peak/cache memory, memory/cache/wired limits, BF16/FP16/FP32 policy,
  cache cleanup, and OOM triage.

- `references/training-patterns.md`
  Training-loop structure, optimizer state, accumulation, checkpointing,
  validation scheduling, progress reporting, and correctness checks.

- `references/inference-patterns.md`
  Generation/inference loops, batching, quantization, cache behavior, warmup,
  streaming, and benchmark hygiene.

- `references/profiling-and-metal.md`
  Metal availability, device info, Xcode GPU capture, custom Metal kernels,
  C++ extensions, and escalation rules.

- `references/portability-bridges.md`
  Swift/C/C++ integration and practical bridge paths for other languages.

- `references/reporting-format.md`
  Required audit report structure and severity/evidence rules.

## Scripts

### `scripts/mlx_audit.py`

Static scanner for Python repos. Inputs:

- Target path.
- Optional include/exclude globs.
- Output format: markdown, json, or both.
- Optional output path.

Candidate findings:

- MLX import sites and likely hot loops.
- `.item()`, `.tolist()`, printing, or NumPy conversion in loops.
- Excessive or suspicious `mx.eval` calls.
- Timing code without clear synchronization/warmup.
- Potential compile-hostile side effects or shape/control-flow hazards.
- Missing memory telemetry near high-impact loops.
- Dtype churn or repeated casts.
- File/folder loops without progress reporting.

Behavior:

- Use Python stdlib by default.
- Report progress with ETA while scanning files.
- Emit markdown for humans and json for follow-on tools.
- Never modify target code.

### `scripts/mlx_env_probe.py`

Environment probe for a target repo. Inputs:

- Target path.
- Optional explicit Python executable.

Behavior:

- Prefer the target repo's `.venv`.
- Report Python executable, architecture, version, and platform.
- Try importing MLX and report MLX version if available.
- Report Metal availability, device info, and memory API availability when MLX
  can be imported.
- Fail with actionable messages instead of suggesting global installs.

### `scripts/mlx_benchmark_template.py`

Copy-ready benchmark harness template. It should include:

- Warmup phase.
- Explicit synchronization/evaluation boundaries.
- Repeated measured runs.
- Correctness hook.
- Memory telemetry hook.
- Markdown/json result output.
- Progress reporting for batched benchmark cases.

## Templates

Create:

- `templates/optimization-report.md`
- `templates/benchmark-notes.md`
- `templates/before-after-verification.md`

Templates must capture:

- Target code path.
- Baseline command and result.
- Change summary.
- After command and result.
- Correctness evidence.
- Runtime and memory evidence.
- Regressions checked.
- Residual risks.

## Error Handling

The plugin must:

- Treat missing `.venv`, missing MLX, non-arm Python, unavailable Metal, dirty
  repo state, and missing benchmark coverage as findings to report.
- Never install Python packages globally.
- Avoid destructive git operations.
- Preserve unrelated user changes.
- Label static findings as candidates until verified.
- Avoid recommending custom kernels without profiling evidence.
- Avoid proposing automatic rewrites when the active code path is not known.
- Give bounded next steps when verification cannot run locally.

## Verification Plan

Implementation is complete only when all relevant checks pass:

- `python3 /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/andrew/Documents/mlx-optimizer-plugin`
- Skill validation for edited skills, using the appropriate skill validator if
  available.
- Python syntax checks for scripts.
- Smoke run `scripts/mlx_audit.py` against a small fixture repo.
- Smoke run `scripts/mlx_env_probe.py` in a fixture with no MLX installed, and
  in a real MLX repo when available without global installation.
- Confirm progress output appears during file/folder scans.
- Confirm generated reports contain evidence, suggested action, verification,
  and residual-risk sections.
- `git status --short` review before commits.

## Release And Versioning

Start plugin version at `0.1.0`. Use semantic versioning:

- Patch for docs/script heuristic fixes.
- Minor for new skills, new scripts, or new report fields.
- Major only for incompatible skill contracts, script CLI changes, or manifest
  structure changes.

During local iteration, use the plugin-creator cachebuster flow only when the
plugin is marketplace-backed and Codex needs to pick up updated plugin metadata.

## Future Extensions

Potential later work:

- Add an MCP server exposing `audit_mlx_project`, `probe_mlx_environment`,
  `generate_mlx_benchmark_plan`, and `summarize_mlx_report`.
- Add richer AST analysis for loop detection and import alias resolution.
- Add project-specific optimization packs for MLX LM, MLX Swift examples, and
  speech/audio workloads.
- Add a benchmark result comparator that summarizes before/after regressions.
- Add generated quick-reference cards or diagrams for MLX lazy evaluation and
  memory behavior.

## Acceptance Criteria

- Repo contains a valid Codex plugin scaffold named `mlx-optimizer`.
- Plugin manifest has concrete metadata, strict semver, valid relative paths,
  and no placeholders.
- Progressive-disclosure skills route MLX tasks without loading irrelevant
  references.
- References cover the MLX optimization surfaces listed above.
- Scripts run without global package installs.
- File/folder scanning scripts report progress with ETA where practical.
- Validation and smoke-test evidence is recorded in the final handoff.
- Work is committed in focused Conventional Commits.
