# Claude Code and Cursor Plugin Support Design

Date: 2026-06-15
Repo: `/Users/andrew/Documents/mlx-optimizer-plugin`

## Goal

Add release-grade install support for Claude Code and Cursor while preserving
the existing canonical `mlx-optimizer` plugin implementation under
`plugins/mlx-optimizer/`.

Release-grade means:

- Native Claude Code and Cursor plugin manifests.
- Marketplace metadata where each tool expects it.
- README installation and validation documentation.
- Packaging tests for the new surfaces.
- Semver bump from `0.1.0` to `0.2.0` across versioned plugin surfaces.

## Current State

The repository currently supports three install surfaces:

| Surface | Current files | Install selector |
| --- | --- | --- |
| Codex | `plugins/mlx-optimizer/.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` | `mlx-optimizer@mlx-optimizer-local` |
| GitHub Copilot CLI | `plugin.json`, `.github/plugin/marketplace.json` | `mlx-optimizer@mlx-optimizer` |
| VS Code Agent Plugins | `plugin.json`, `.github/plugin/marketplace.json` | Source install or `mlx-optimizer@mlx-optimizer` |

The canonical skills, scripts, references, and templates already live under
`plugins/mlx-optimizer/`. Existing packaging tests validate that Codex and
Copilot marketplace entries resolve to the expected manifests and skills.

## External Documentation Basis

This design is based on the current documentation reviewed on 2026-06-15:

- OpenAI Codex plugins: `https://developers.openai.com/codex/plugins/build`
- GitHub Copilot CLI plugin reference:
  `https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference`
- VS Code Agent Plugins:
  `https://code.visualstudio.com/docs/agent-customization/agent-plugins`
- Claude Code plugins: `https://code.claude.com/docs/en/plugins`
- Claude Code marketplaces:
  `https://code.claude.com/docs/en/plugin-marketplaces`
- Cursor plugins: `https://cursor.com/docs/plugins.md`
- Cursor Agent Skills: `https://cursor.com/docs/skills.md`

## Chosen Approach

Use native manifests for Claude Code and Cursor, with both tools pointing at
the existing canonical plugin root.

This avoids copying skills into tool-specific directories. It keeps one source
of truth for:

- `skills/`
- `scripts/`
- `references/`
- `templates/`

## File Layout

Add these files:

```text
.claude-plugin/
  marketplace.json
.cursor-plugin/
  marketplace.json
plugins/mlx-optimizer/
  .claude-plugin/
    plugin.json
  .cursor-plugin/
    plugin.json
```

Keep existing files:

```text
.agents/plugins/marketplace.json
.github/plugin/marketplace.json
plugin.json
plugins/mlx-optimizer/.codex-plugin/plugin.json
plugins/mlx-optimizer/skills/
plugins/mlx-optimizer/scripts/
plugins/mlx-optimizer/references/
plugins/mlx-optimizer/templates/
```

## Claude Code Support

Claude Code expects plugin manifests under `.claude-plugin/plugin.json` inside
the plugin root, and marketplace catalogs under `.claude-plugin/marketplace.json`
at the marketplace root.

Add `plugins/mlx-optimizer/.claude-plugin/plugin.json` with:

- `name`: `mlx-optimizer`
- `description`: same purpose summary as the existing manifests
- `version`: `0.2.0`
- `author.name`: `Andrew`
- `license`: `MIT`
- `keywords`: existing MLX keyword list
- `skills`: `./skills/`

Add `.claude-plugin/marketplace.json` with:

- top-level `name`: `mlx-optimizer`
- `owner.name`: `Andrew`
- `description`: marketplace description for Claude Code
- `plugins[0].name`: `mlx-optimizer`
- `plugins[0].source`: `./plugins/mlx-optimizer`
- plugin metadata matching the manifest where useful

Document install commands:

```bash
claude plugin marketplace add sealad886/mlx-optimizer-plugin
claude plugin install mlx-optimizer@mlx-optimizer
```

For local development:

```bash
claude plugin marketplace add /Users/andrew/Documents/mlx-optimizer-plugin
claude plugin install mlx-optimizer@mlx-optimizer
```

## Cursor Support

Cursor expects plugin manifests under `.cursor-plugin/plugin.json`. For
multi-plugin repositories and team marketplace workflows, Cursor uses
`.cursor-plugin/marketplace.json`.

Add `plugins/mlx-optimizer/.cursor-plugin/plugin.json` with:

- `name`: `mlx-optimizer`
- `description`: same purpose summary as the existing manifests
- `version`: `0.2.0`
- `author.name`: `Andrew`
- `license`: `MIT`
- `keywords`: existing MLX keyword list
- `skills`: `./skills/`

Add `.cursor-plugin/marketplace.json` with:

- top-level `name`: `mlx-optimizer`
- `owner.name`: `Andrew`
- `description`: marketplace description for Cursor
- `plugins[0].name`: `mlx-optimizer`
- `plugins[0].source`: `./plugins/mlx-optimizer`
- plugin metadata matching the manifest where useful

Document local plugin development using a symlink or copy into
`~/.cursor/plugins/local/mlx-optimizer`, with the plugin root being
`plugins/mlx-optimizer/`. Document marketplace/team use without claiming public
Cursor Marketplace publication unless that submission happens later.

## Versioning

This is a new install capability, so bump versioned plugin surfaces from
`0.1.0` to `0.2.0`:

- `plugin.json`
- `.github/plugin/marketplace.json`
- `plugins/mlx-optimizer/.codex-plugin/plugin.json`
- `plugins/mlx-optimizer/.claude-plugin/plugin.json`
- `plugins/mlx-optimizer/.cursor-plugin/plugin.json`
- marketplace plugin entries that include `version`

Do not add a version to `.agents/plugins/marketplace.json`; current Codex
marketplace policy metadata there is separate from plugin release metadata.

## Documentation Updates

Update `README.md`:

- Add Claude Code and Cursor to the supported plugin surfaces table.
- Add Claude Code install commands.
- Add Cursor local and marketplace/team install guidance.
- Add new manifest paths to repository layout.
- Add JSON validation commands for the new manifests.
- Keep Codex, Copilot CLI, and VS Code instructions intact.

Update `.github/copilot-instructions.md`:

- Add Claude Code and Cursor to the repository overview.
- Add new manifest validation commands.
- Update packaging conventions to preserve all supported manifest layers.

Update issue templates:

- Add Claude Code and Cursor checkboxes to install/runtime and feature-request
  surface lists.

## Testing

Extend `PluginPackagingTests` in `tests/test_mlx_tools.py`.

New assertions:

- Claude plugin manifest exists at
  `plugins/mlx-optimizer/.claude-plugin/plugin.json`.
- Claude manifest has `name == "mlx-optimizer"`, `version == "0.2.0"`, and
  a `skills` path resolving to `plugins/mlx-optimizer/skills/`.
- Claude marketplace exists at `.claude-plugin/marketplace.json`.
- Claude marketplace has `name == "mlx-optimizer"` and source
  `./plugins/mlx-optimizer`.
- Cursor plugin manifest exists at
  `plugins/mlx-optimizer/.cursor-plugin/plugin.json`.
- Cursor manifest has `name == "mlx-optimizer"`, `version == "0.2.0"`, and
  a `skills` path resolving to `plugins/mlx-optimizer/skills/`.
- Cursor marketplace exists at `.cursor-plugin/marketplace.json`.
- Cursor marketplace has `name == "mlx-optimizer"` and source
  `./plugins/mlx-optimizer`.
- Existing Codex and Copilot tests continue to pass with the version bump.

Validation commands:

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

Optional local tool validation, when installed:

```bash
claude plugin validate /Users/andrew/Documents/mlx-optimizer-plugin
claude plugin validate /Users/andrew/Documents/mlx-optimizer-plugin/plugins/mlx-optimizer
```

Cursor does not currently provide an equivalent repo-local CLI validator in the
reviewed docs. Validate Cursor support by JSON checks and path-resolution tests,
then smoke test in Cursor manually when available.

## Out of Scope

- Gemini CLI extension support.
- Windsurf/Cascade, Cline, Aider, Junie, or Roo Code adapters.
- MCP server wrapper around the existing Python scripts.
- New skills, new MLX behavior, or changes to existing script output.
- Public Cursor Marketplace submission.
- GitHub release creation.

## Risks and Mitigations

Risk: Claude and Cursor plugin schemas may evolve while these features are new.
Mitigation: keep manifests minimal and aligned with documented required fields;
validate with JSON and path tests, and document any manual smoke-test gap.

Risk: Multiple marketplace files can confuse future maintainers.
Mitigation: update README and Copilot instructions with a support matrix and
clear ownership for each manifest root.

Risk: Version drift across surfaces.
Mitigation: tests should assert version alignment for all versioned manifests.

Risk: Cursor public marketplace claims could overstate support.
Mitigation: document local/team marketplace support only, unless public Cursor
submission is completed later.

## Acceptance Criteria

- Claude Code can discover the plugin through the repo marketplace metadata.
- Cursor can load the plugin from the canonical plugin root and has marketplace
  metadata for team or multi-plugin repository workflows.
- Existing Codex, GitHub Copilot CLI, and VS Code support remains intact.
- All versioned manifests report `0.2.0`.
- README and contributor-facing instructions describe all supported surfaces.
- Packaging tests cover all manifest and marketplace paths.
- Final handoff includes concrete verification commands, outcomes, and bounded
  residual risks.
