# Contributing

Contributions should keep this repo focused: a small, installable MLX
optimization plugin with evidence-based skills, references, scripts, templates,
and packaging metadata.

## Workflow

1. Fork or branch from `main`.
2. Keep changes scoped to one logical topic.
3. Use the repo-local `.venv` for Python commands.
4. Add or update tests when behavior changes.
5. Update README or reference docs when user-facing behavior changes.
6. Commit with a Conventional Commits message.
7. Open a pull request using the template in `.github/PULL_REQUEST_TEMPLATE.md`.

## Local Environment

Never install Python packages globally. Create and use `.venv` from the project
root:

```bash
python3 -m venv .venv
.venv/bin/python --version
```

This repo currently uses Python stdlib scripts and stdlib `unittest` tests. If
a future change needs third-party Python packages, add an explicit dependency
file and document the `.venv` install command.

## Validation

Run the baseline checks before opening a PR:

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

When available on your machine, also run the Codex plugin and skill validators:

```bash
.venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/mlx-optimizer
for skill in plugins/mlx-optimizer/skills/*; do
  .venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
done
```

## Coding Standards

- Reuse existing skills, references, and scripts before adding new ones.
- Keep scripts conservative and dependency-light.
- Treat static scanner output as candidate findings, not proven regressions.
- Preserve unrelated local changes.
- Any code path that loops over files or folders must report user-visible
  progress and include ETA where a reasonable estimate is possible.
- Prefer markdown templates and structured JSON output over ad hoc prose when
  another tool or agent may consume results.

## Documentation

Update docs when a change affects:

- Installation selectors or manifest paths.
- Skill routing or reference file responsibilities.
- Script arguments, output formats, or progress behavior.
- Validation commands or release steps.

## License

By contributing, you agree that your contributions are licensed under the MIT
License. See [LICENSE](LICENSE).
