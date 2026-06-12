# MLX Optimizer Plugin

Repo-local Codex plugin for Python-first MLX optimization on Apple Silicon.

The plugin source lives in `plugins/mlx-optimizer/` so the plugin folder name
matches the manifest name. It provides progressive-disclosure skills, MLX
optimization references, stdlib-only audit scripts, benchmark templates, and
smoke tests.

## Installability

This repository is structured for both Codex and GitHub Copilot plugin
installers.

- `plugins/mlx-optimizer/.codex-plugin/plugin.json` is the Codex plugin
  manifest.
- `.agents/plugins/marketplace.json` is the repo-local Codex marketplace.
- `plugin.json` is the GitHub Copilot CLI and VS Code Agent Plugin manifest.
- `.github/plugin/marketplace.json` is the GitHub Copilot CLI and VS Code
  marketplace entry.

### Codex

From this checkout, register the local marketplace and install the plugin:

```bash
codex plugin marketplace add /Users/andrew/Documents/mlx-optimizer-plugin
codex plugin add mlx-optimizer@mlx-optimizer-local
```

For a hosted repository, add the marketplace source by repository name or Git
URL, then install the same selector:

```bash
codex plugin marketplace add OWNER/REPO
codex plugin add mlx-optimizer@mlx-optimizer-local
```

### GitHub Copilot CLI

Register the marketplace and install the plugin:

```bash
copilot plugin marketplace add OWNER/REPO
copilot plugin install mlx-optimizer@mlx-optimizer
```

For local development, register this checkout as the marketplace source:

```bash
copilot plugin marketplace add /Users/andrew/Documents/mlx-optimizer-plugin
copilot plugin install mlx-optimizer@mlx-optimizer
```

Direct local installs also work for development, but Copilot CLI warns that
direct plugin installs are deprecated in favor of marketplace installs:

```bash
copilot plugin install /Users/andrew/Documents/mlx-optimizer-plugin
```

### VS Code Agent Plugins

VS Code can install the same plugin from source with
`Chat: Install Plugin From Source`, using the repository Git URL.

To browse it as a marketplace plugin, add the hosted repository to VS Code
settings:

```json
{
  "chat.plugins.marketplaces": [
    "OWNER/REPO"
  ]
}
```

For local development, register this checkout in user or workspace settings:

```json
{
  "chat.pluginLocations": {
    "/Users/andrew/Documents/mlx-optimizer-plugin": true
  }
}
```

## Layout

- `plugin.json` is the GitHub Copilot CLI and VS Code plugin manifest.
- `.github/plugin/marketplace.json` is the Copilot/VS Code marketplace file.
- `.agents/plugins/marketplace.json` is the Codex marketplace file.
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
.venv/bin/python /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer
.venv/bin/python -m json.tool plugin.json >/dev/null
.venv/bin/python -m json.tool .github/plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .agents/plugins/marketplace.json >/dev/null
```

Do not install Python packages globally.

## Validation Evidence

Before handing off implementation, run:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py
.venv/bin/python /Users/andrew/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mlx-optimizer
.venv/bin/python -m json.tool plugin.json >/dev/null
.venv/bin/python -m json.tool .github/plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .agents/plugins/marketplace.json >/dev/null
for skill in plugins/mlx-optimizer/skills/*; do .venv/bin/python /Users/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"; done
```

Record command outcomes in the final response.
