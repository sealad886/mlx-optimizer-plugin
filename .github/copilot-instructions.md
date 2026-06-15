---
last_updated_commit: "ae932c4"
last_updated_date: "2026-06-15"
schema_version: 1
---

# Copilot Coding Agent Instructions

## 0. Staleness Check

Before starting substantial work, compare this file with the current repo:

```bash
LAST_UPDATED_COMMIT="$(sed -n 's/^last_updated_commit: "\(.*\)"/\1/p' .github/copilot-instructions.md)"
git log --oneline "${LAST_UPDATED_COMMIT}..HEAD"
```

If more than 20 commits have landed since `last_updated_commit`, or this file
is more than 30 days old, refresh it as part of the change. Update the metadata
above after refreshing.

## 1. Repository Overview

This repository packages `mlx-optimizer`, a Python-first MLX optimization plugin
for Apple Silicon. It targets Codex, GitHub Copilot CLI, VS Code Agent Plugins,
Claude Code, and Cursor. The plugin provides skills, references, scripts, and templates for
evidence-based MLX audits, training-loop optimization, inference optimization,
Metal profiling escalation, and language-boundary guidance.

The canonical plugin implementation is in `plugins/mlx-optimizer/`. Root-level
metadata exists for Copilot/VS Code packaging, and tool-specific marketplace
files exist for Codex, Claude Code, and Cursor.

## 2. Build, Test, and Lint

Never install Python packages globally. Use the repo-local `.venv`:

```bash
python3 -m venv .venv
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

When Codex system validators are available locally, also run:

```bash
.venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/mlx-optimizer
for skill in plugins/mlx-optimizer/skills/*; do
  .venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
done
```

There is no package install step today. Scripts use the Python standard library.

## 3. Project Layout

```text
plugin.json                                      Copilot/VS Code plugin manifest
.agents/plugins/marketplace.json                Codex marketplace entry
.claude-plugin/marketplace.json                 Claude Code marketplace entry
.cursor-plugin/marketplace.json                 Cursor marketplace entry
.github/plugin/marketplace.json                 Copilot/VS Code marketplace entry
plugins/mlx-optimizer/.codex-plugin/plugin.json Codex plugin manifest
plugins/mlx-optimizer/.claude-plugin/plugin.json Claude Code plugin manifest
plugins/mlx-optimizer/.cursor-plugin/plugin.json Cursor plugin manifest
plugins/mlx-optimizer/skills/                   Skill entrypoints
plugins/mlx-optimizer/references/               Task-routed MLX references
plugins/mlx-optimizer/scripts/                  Audit, environment probe, benchmark template
plugins/mlx-optimizer/templates/                Report and verification templates
tests/test_mlx_tools.py                         Unit tests for scripts and packaging
docs/superpowers/                               Original design spec and plan
```

## 4. CI and Automation

`.github/workflows/ci.yml` runs unit tests, script compilation, and JSON manifest
validation on Python 3.11, 3.12, and 3.13.

`.github/workflows/codeql-analysis.yml` runs Python CodeQL analysis on push,
pull request, weekly schedule, and manual dispatch.

`.github/workflows/stale.yml` marks inactive issues and PRs stale after 60 days
and closes them after 7 more days.

`.github/dependabot.yml` keeps GitHub Actions dependencies current.

## 5. Conventions

- Preserve the packaging layers: Codex uses `plugins/mlx-optimizer/` plus
  `.agents/plugins/marketplace.json`; Copilot/VS Code uses root `plugin.json`
  plus `.github/plugin/marketplace.json`; Claude Code uses
  `plugins/mlx-optimizer/.claude-plugin/plugin.json` plus
  `.claude-plugin/marketplace.json`; Cursor uses
  `plugins/mlx-optimizer/.cursor-plugin/plugin.json` plus
  `.cursor-plugin/marketplace.json`.
- Keep version numbers aligned across versioned manifests.
- Reuse existing skills, references, scripts, and templates before adding new
  parallel paths.
- Treat static MLX audit findings as candidate findings until benchmarked.
- Any script path that loops over files or folders must report user-visible
  progress and include ETA where practical.
- Use Conventional Commits for commit messages.

Trust these instructions. Search the repo again when a task touches an area not
covered here or when current files contradict this summary.
