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

## Validation Evidence

Before handing off implementation, run:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py
python3 /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer
for skill in plugins/mlx-optimizer/skills/*; do python3 /Users/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"; done
```
