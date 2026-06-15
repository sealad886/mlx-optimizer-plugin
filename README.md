# MLX Optimizer Plugin

`mlx-optimizer` is a plugin bundle for optimizing Python-first
[MLX](https://github.com/ml-explore/mlx) projects on Apple Silicon. It gives
Codex, GitHub Copilot CLI, VS Code Agent Plugins, Claude Code, and Cursor a
focused set of skills, reference notes, audit scripts, and report templates for
MLX performance work.

The plugin is intentionally evidence-driven. It helps an agent inspect a target
repo, identify candidate performance and correctness risks, and verify changes
with concrete commands, timings, memory telemetry, correctness checks, and
residual-risk notes. Static findings are treated as candidates until the target
workload proves them.

## What This Plugin Provides

- Progressive-disclosure MLX skills for audits, training loops, inference loops,
  Metal profiling, custom-kernel escalation, and language-boundary guidance.
- Compact MLX reference files covering lazy evaluation, synchronization,
  transforms, memory, dtype policy, benchmark hygiene, and reporting.
- Stdlib-only Python utilities for static MLX audits, repo-local environment
  probing, and copy-ready benchmark scaffolding.
- Markdown templates for optimization reports, benchmark notes, and before/after
  verification.
- Packaging for Codex, GitHub Copilot/VS Code, Claude Code, and Cursor plugin
  installers.
- Smoke tests that validate script behavior and packaging paths without needing
  MLX to be installed.

## Supported Plugin Surfaces

This repository contains multiple plugin packaging layers. Keep them distinct when
editing manifests or release metadata.

| Surface | Files | Install selector |
| --- | --- | --- |
| Codex | `plugins/mlx-optimizer/.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` | `mlx-optimizer@mlx-optimizer-local` |
| GitHub Copilot CLI / VS Code Agent Plugins | `plugin.json` and `.github/plugin/marketplace.json` | `mlx-optimizer@mlx-optimizer` |
| Claude Code | `plugins/mlx-optimizer/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` | `mlx-optimizer@mlx-optimizer` |
| Cursor | `plugins/mlx-optimizer/.cursor-plugin/plugin.json` and `.cursor-plugin/marketplace.json` | Local/team marketplace plugin |

The canonical plugin implementation lives in `plugins/mlx-optimizer/`. The root
`plugin.json` exists so Copilot and VS Code can resolve the same skill bundle
from the repository root. Claude Code and Cursor use tool-specific manifests
inside the canonical plugin root and marketplace files at the repository root.

## Installation

### Codex From This Checkout

```bash
codex plugin marketplace add /path/to/mlx-optimizer-plugin --json
codex plugin add mlx-optimizer@mlx-optimizer-local --json
```

### Codex From GitHub

```bash
codex plugin marketplace add sealad886/mlx-optimizer-plugin --json
codex plugin add mlx-optimizer@mlx-optimizer-local --json
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add sealad886/mlx-optimizer-plugin
copilot plugin install mlx-optimizer@mlx-optimizer
```

For local development, register this checkout as the marketplace source:

```bash
copilot plugin marketplace add /path/to/mlx-optimizer-plugin
copilot plugin install mlx-optimizer@mlx-optimizer
```

Direct local installs can still be useful while developing the plugin, but the
Copilot CLI prefers marketplace-based installs:

```bash
copilot plugin install /path/to/mlx-optimizer-plugin
```

### Claude Code

```bash
claude plugin marketplace add sealad886/mlx-optimizer-plugin
claude plugin install mlx-optimizer@mlx-optimizer
```

For local development, register this checkout:

```bash
claude plugin marketplace add /path/to/mlx-optimizer-plugin
claude plugin install mlx-optimizer@mlx-optimizer
```

### VS Code Agent Plugins

Install from source with the VS Code command palette action
`Chat: Install Plugin From Source`, then use this repository URL:

```text
https://github.com/sealad886/mlx-optimizer-plugin
```

To browse it through a marketplace source, add the hosted repository to VS Code
settings:

```json
{
  "chat.plugins.marketplaces": [
    "sealad886/mlx-optimizer-plugin"
  ]
}
```

For local plugin development, register this checkout:

```json
{
  "chat.pluginLocations": {
    "/path/to/mlx-optimizer-plugin": true
  }
}
```

### Cursor

For local plugin development, symlink the canonical plugin root into Cursor's
local plugin directory:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s /path/to/mlx-optimizer-plugin/plugins/mlx-optimizer ~/.cursor/plugins/local/mlx-optimizer
```

Then restart Cursor or run `Developer: Reload Window`.

For team marketplace distribution, use Cursor's dashboard marketplace import
flow with this repository. Cursor reads `.cursor-plugin/marketplace.json` at
the repository root and loads `plugins/mlx-optimizer/.cursor-plugin/plugin.json`
from the plugin source path. This repository does not claim public Cursor
Marketplace publication until that submission is completed separately.

## Skill Guide

The entry-point skill is `mlx-optimizer`. It routes work to focused specialist
skills and the minimum reference files needed for the task.

| Skill | Use it for |
| --- | --- |
| `mlx-optimizer` | Routing MLX optimization, audit, profiling, benchmark, or explanation work. |
| `mlx-performance-audit` | Repo-wide MLX performance reviews and unknown bottlenecks. |
| `mlx-training-optimizer` | Training loops, `value_and_grad`, optimizer state, accumulation, checkpointing, validation cadence, dtype policy, and progress reporting. |
| `mlx-inference-optimizer` | Inference, generation, serving loops, batching, cache behavior, quantization, streaming sync, and latency/throughput checks. |
| `mlx-metal-kernels` | MLX Metal capture, `mx.fast`, custom Metal kernels, and C++ extension escalation after profiling evidence exists. |
| `mlx-portability-bridges` | Swift, C, C++, subprocess, service, C ABI, Core ML, and other boundaries around Python-first MLX work. |

Example prompts:

```text
Audit this repo for MLX performance issues.
Optimize this MLX training loop and verify with a short smoke run.
Check whether this benchmark is timing scheduled MLX work or completed work.
Decide whether this bottleneck justifies a custom Metal kernel.
Explain the safest way to bridge this Python MLX model into a Swift app.
```

## Included Scripts

All scripts are dependency-light Python utilities. They should run from a target
project's repo-local `.venv`; never install Python packages globally.

### `mlx_env_probe.py`

Probe a target repo's Python and MLX environment.

```bash
.venv/bin/python plugins/mlx-optimizer/scripts/mlx_env_probe.py /path/to/target --format markdown
.venv/bin/python plugins/mlx-optimizer/scripts/mlx_env_probe.py /path/to/target --python /path/to/target/.venv/bin/python --format json
```

The probe reports Python executable, prefix, version, platform, MLX import
status, Metal availability, device information, and MLX memory API availability.
When the target repo has no `.venv`, it returns a `missing-venv` status and a
repo-local setup recommendation.

### `mlx_audit.py`

Scan Python files for candidate MLX performance findings.

```bash
.venv/bin/python plugins/mlx-optimizer/scripts/mlx_audit.py /path/to/target --format markdown
.venv/bin/python plugins/mlx-optimizer/scripts/mlx_audit.py /path/to/target --format json --output reports/mlx-audit.json
```

The scanner reports progress to stderr with an ETA while scanning files. Current
candidate categories include:

- `sync-in-loop`: `.item()`, `.tolist()`, or `.numpy()` inside loops.
- `eval-in-loop`: `mx.eval` or imported eval aliases inside loops.
- `benchmark-missing-eval`: timing code in an MLX file without an evaluation
  boundary in the timed function.
- `syntax-error` and `read-error`: files that could not be scanned reliably.

The audit never edits target code.

### `mlx_benchmark_template.py`

Generate a copy-ready benchmark scaffold with warmup, repeated measured runs,
explicit synchronization, correctness checking, memory snapshots, and progress
output with ETA.

```bash
.venv/bin/python plugins/mlx-optimizer/scripts/mlx_benchmark_template.py --runs 5 --warmup 2 --format markdown
.venv/bin/python plugins/mlx-optimizer/scripts/mlx_benchmark_template.py --runs 10 --warmup 3 --format json --output reports/benchmark.json
```

Replace the placeholder `workload()` function with the target operation when
copying the template into another repo.

## Repository Layout

```text
.
├── plugin.json
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
├── .cursor-plugin/marketplace.json
├── .github/plugin/marketplace.json
├── plugins/mlx-optimizer/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── .cursor-plugin/plugin.json
│   ├── skills/
│   ├── references/
│   ├── scripts/
│   └── templates/
├── tests/
│   ├── fixtures/
│   └── test_mlx_tools.py
└── docs/superpowers/
    ├── specs/
    └── plans/
```

Important paths:

- `plugins/mlx-optimizer/skills/`: Codex/Copilot skill entrypoints.
- `plugins/mlx-optimizer/references/`: task-routed MLX guidance used by skills.
- `plugins/mlx-optimizer/scripts/`: executable audit, probe, and benchmark
  utilities.
- `plugins/mlx-optimizer/templates/`: copy-ready report and benchmark templates.
- `tests/test_mlx_tools.py`: stdlib `unittest` coverage for scripts and
  packaging metadata.
- `docs/superpowers/specs/`: design rationale for the initial plugin.
- `docs/superpowers/plans/`: implementation plan used to build the first
  version.

## Development Setup

Use the repository virtual environment for Python work.

```bash
python3 -m venv .venv
.venv/bin/python --version
```

This repo has no runtime dependency file today. Do not install Python packages
globally. If future tests need third-party packages, add an explicit dependency
file and install into `.venv` only.

## Validation

Run these checks before handing off changes:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py
.venv/bin/python -m json.tool plugin.json >/dev/null
.venv/bin/python -m json.tool .github/plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .agents/plugins/marketplace.json >/dev/null
.venv/bin/python -m json.tool .claude-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .cursor-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.codex-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.claude-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.cursor-plugin/plugin.json >/dev/null
```

When Codex system skills are available locally, also run:

```bash
.venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/mlx-optimizer
for skill in plugins/mlx-optimizer/skills/*; do
  .venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
done
```

For packaging changes, add isolated install smoke tests when possible:

```bash
codex plugin marketplace add /path/to/mlx-optimizer-plugin --json
codex plugin add mlx-optimizer@mlx-optimizer-local --json
copilot plugin marketplace add /path/to/mlx-optimizer-plugin
copilot plugin install mlx-optimizer@mlx-optimizer
claude plugin marketplace add /path/to/mlx-optimizer-plugin
claude plugin install mlx-optimizer@mlx-optimizer
```

## Release Checklist

This repo currently uses semantic versioning across plugin manifests. For a
release, update every versioned surface that applies:

- `plugin.json`
- `.github/plugin/marketplace.json`
- `.claude-plugin/marketplace.json`
- `.cursor-plugin/marketplace.json`
- `plugins/mlx-optimizer/.codex-plugin/plugin.json`
- `plugins/mlx-optimizer/.claude-plugin/plugin.json`
- `plugins/mlx-optimizer/.cursor-plugin/plugin.json`
- README installation or compatibility notes, when behavior changes

Before tagging or publishing:

1. Run local validation commands.
2. Run plugin validators if available.
3. Smoke install through Codex and Copilot marketplace paths when the change
   affects packaging.
4. Confirm `.agents/plugins/marketplace.json`, `.github/plugin/marketplace.json`,
   `.claude-plugin/marketplace.json`, and `.cursor-plugin/marketplace.json`
   still point to existing manifests.
5. Commit with a Conventional Commits message.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution workflow and local
checks. The short version:

- Reuse existing skills, references, and scripts before adding parallel paths.
- Keep scripts stdlib-only unless the repo gains an explicit dependency file.
- Any code path that loops over files or folders must report user-visible
  progress and include ETA where a reasonable estimate is possible.
- Document commands, outcomes, and bounded residual risks in final handoffs.

## Security

This plugin can guide agents that edit code in other repositories. Treat
recommendations as advisory until they are verified against the target workload.
Report vulnerabilities through GitHub Security Advisories rather than public
issues. See [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
