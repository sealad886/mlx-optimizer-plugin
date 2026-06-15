# Claude Cursor Plugin Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add release-grade Claude Code and Cursor install support for the MLX Optimizer plugin.

**Architecture:** Keep `plugins/mlx-optimizer/` as the canonical plugin root. Add Claude and Cursor manifests/marketplaces that point to that root, then update tests, docs, CI validation, and version metadata to `0.2.0`.

**Tech Stack:** JSON plugin manifests, Markdown docs, Python stdlib `unittest`, GitHub Actions, shell validation through repo-local `.venv`.

---

## File Structure

- Modify: `tests/test_mlx_tools.py`
  - Owns packaging path tests and version-alignment checks.
- Create: `.claude-plugin/marketplace.json`
  - Claude Code marketplace catalog at repository root.
- Create: `.cursor-plugin/marketplace.json`
  - Cursor marketplace catalog at repository root.
- Create: `plugins/mlx-optimizer/.claude-plugin/plugin.json`
  - Claude Code plugin manifest at canonical plugin root.
- Create: `plugins/mlx-optimizer/.cursor-plugin/plugin.json`
  - Cursor plugin manifest at canonical plugin root.
- Modify: `plugin.json`
  - Root Copilot/VS Code manifest version bump.
- Modify: `.github/plugin/marketplace.json`
  - Copilot/VS Code marketplace version bump and metadata description.
- Modify: `plugins/mlx-optimizer/.codex-plugin/plugin.json`
  - Codex manifest version bump.
- Modify: `README.md`
  - Support matrix, install docs, layout, validation commands, release checklist.
- Modify: `.github/copilot-instructions.md`
  - Future-agent packaging guidance and validation commands.
- Modify: `.github/ISSUE_TEMPLATE/bug_report.md`
  - Add Claude Code and Cursor surfaces.
- Modify: `.github/ISSUE_TEMPLATE/feature_request.md`
  - Add Claude Code and Cursor target surfaces.
- Modify: `.github/workflows/ci.yml`
  - Validate new JSON manifests in CI.

## Task 1: Packaging Tests First

**Files:**
- Modify: `tests/test_mlx_tools.py`

- [ ] **Step 1: Add packaging constants**

Add these constants after the existing `CODEX_MARKETPLACE` constant:

```python
PLUGIN_ROOT = ROOT / "plugins" / "mlx-optimizer"
CODEX_PLUGIN_JSON = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CLAUDE_PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
CURSOR_MARKETPLACE = ROOT / ".cursor-plugin" / "marketplace.json"
CURSOR_PLUGIN_JSON = PLUGIN_ROOT / ".cursor-plugin" / "plugin.json"
EXPECTED_PLUGIN_VERSION = "0.2.0"
```

- [ ] **Step 2: Replace `PluginPackagingTests` with release-grade checks**

Replace the full `PluginPackagingTests` class with this implementation:

```python
class PluginPackagingTests(unittest.TestCase):
    def assert_manifest_points_to_existing_skills(self, manifest_path, manifest_root):
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(payload["name"], "mlx-optimizer")
        self.assertEqual(payload["version"], EXPECTED_PLUGIN_VERSION)
        skills_path = (manifest_root / payload["skills"]).resolve()
        self.assertTrue(skills_path.is_dir(), skills_path)
        self.assertTrue((skills_path / "mlx-optimizer" / "SKILL.md").is_file())
        return payload

    def assert_marketplace_points_to_plugin(self, marketplace_path, marker_dir):
        payload = json.loads(marketplace_path.read_text(encoding="utf-8"))

        self.assertEqual(payload["name"], "mlx-optimizer")
        self.assertEqual(payload["plugins"][0]["name"], "mlx-optimizer")
        self.assertEqual(payload["plugins"][0]["version"], EXPECTED_PLUGIN_VERSION)
        source = payload["plugins"][0]["source"]
        self.assertEqual(source, "./plugins/mlx-optimizer")
        manifest = (ROOT / source / marker_dir / "plugin.json").resolve()
        self.assertTrue(manifest.is_file(), manifest)
        return payload

    def test_copilot_root_plugin_points_to_existing_skills(self):
        payload = self.assert_manifest_points_to_existing_skills(
            ROOT_PLUGIN_JSON, ROOT
        )

        self.assertEqual(payload["skills"], "plugins/mlx-optimizer/skills/")

    def test_copilot_marketplace_points_to_root_plugin(self):
        payload = json.loads(COPILOT_MARKETPLACE.read_text(encoding="utf-8"))

        self.assertEqual(payload["name"], "mlx-optimizer")
        self.assertEqual(payload["metadata"]["version"], EXPECTED_PLUGIN_VERSION)
        self.assertEqual(payload["plugins"][0]["name"], "mlx-optimizer")
        self.assertEqual(payload["plugins"][0]["version"], EXPECTED_PLUGIN_VERSION)
        source = payload["plugins"][0]["source"]
        self.assertTrue((ROOT / source / "plugin.json").resolve().is_file())

    def test_codex_plugin_manifest_points_to_existing_skills(self):
        payload = self.assert_manifest_points_to_existing_skills(
            CODEX_PLUGIN_JSON, PLUGIN_ROOT
        )

        self.assertEqual(payload["skills"], "./skills/")

    def test_codex_marketplace_points_to_codex_plugin(self):
        payload = json.loads(CODEX_MARKETPLACE.read_text(encoding="utf-8"))

        self.assertEqual(payload["name"], "mlx-optimizer-local")
        self.assertEqual(payload["plugins"][0]["name"], "mlx-optimizer")
        source = payload["plugins"][0]["source"]["path"]
        self.assertTrue((ROOT / source / ".codex-plugin" / "plugin.json").resolve().is_file())

    def test_claude_plugin_manifest_points_to_existing_skills(self):
        payload = self.assert_manifest_points_to_existing_skills(
            CLAUDE_PLUGIN_JSON, PLUGIN_ROOT
        )

        self.assertEqual(payload["skills"], "./skills/")

    def test_claude_marketplace_points_to_claude_plugin(self):
        self.assert_marketplace_points_to_plugin(
            CLAUDE_MARKETPLACE, ".claude-plugin"
        )

    def test_cursor_plugin_manifest_points_to_existing_skills(self):
        payload = self.assert_manifest_points_to_existing_skills(
            CURSOR_PLUGIN_JSON, PLUGIN_ROOT
        )

        self.assertEqual(payload["skills"], "./skills/")

    def test_cursor_marketplace_points_to_cursor_plugin(self):
        self.assert_marketplace_points_to_plugin(
            CURSOR_MARKETPLACE, ".cursor-plugin"
        )
```

- [ ] **Step 3: Run packaging tests and verify they fail**

Run:

```bash
.venv/bin/python -m unittest tests.test_mlx_tools.PluginPackagingTests -v
```

Expected: fail because `plugin.json` still reports `0.1.0` and the Claude/Cursor manifest paths do not exist.

- [ ] **Step 4: Commit failing packaging tests**

Run:

```bash
git add tests/test_mlx_tools.py
git diff --cached --check
git commit -m "test: cover Claude and Cursor plugin packaging"
```

Expected: commit succeeds with only `tests/test_mlx_tools.py` staged.

## Task 2: Add Manifests and Version Bump

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `.cursor-plugin/marketplace.json`
- Create: `plugins/mlx-optimizer/.claude-plugin/plugin.json`
- Create: `plugins/mlx-optimizer/.cursor-plugin/plugin.json`
- Modify: `plugin.json`
- Modify: `.github/plugin/marketplace.json`
- Modify: `plugins/mlx-optimizer/.codex-plugin/plugin.json`

- [ ] **Step 1: Create Claude plugin manifest**

Create `plugins/mlx-optimizer/.claude-plugin/plugin.json`:

```json
{
  "name": "mlx-optimizer",
  "version": "0.2.0",
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
  "category": "Productivity",
  "skills": "./skills/"
}
```

- [ ] **Step 2: Create Claude marketplace**

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "mlx-optimizer",
  "description": "MLX optimization plugin marketplace for Claude Code.",
  "owner": {
    "name": "Andrew"
  },
  "plugins": [
    {
      "name": "mlx-optimizer",
      "description": "Python-first MLX optimization skills, references, and audit scripts for Apple Silicon.",
      "version": "0.2.0",
      "source": "./plugins/mlx-optimizer",
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
      "category": "Productivity",
      "skills": "./skills/"
    }
  ]
}
```

- [ ] **Step 3: Create Cursor plugin manifest**

Create `plugins/mlx-optimizer/.cursor-plugin/plugin.json`:

```json
{
  "name": "mlx-optimizer",
  "version": "0.2.0",
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
  "category": "Productivity",
  "skills": "./skills/"
}
```

- [ ] **Step 4: Create Cursor marketplace**

Create `.cursor-plugin/marketplace.json`:

```json
{
  "name": "mlx-optimizer",
  "description": "MLX optimization plugin marketplace for Cursor.",
  "owner": {
    "name": "Andrew"
  },
  "plugins": [
    {
      "name": "mlx-optimizer",
      "description": "Python-first MLX optimization skills, references, and audit scripts for Apple Silicon.",
      "version": "0.2.0",
      "source": "./plugins/mlx-optimizer",
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
      "category": "Productivity",
      "skills": "./skills/"
    }
  ]
}
```

- [ ] **Step 5: Bump root Copilot/VS Code manifest**

Modify `plugin.json` so only `version` changes:

```json
"version": "0.2.0"
```

- [ ] **Step 6: Bump Copilot/VS Code marketplace versions**

Modify `.github/plugin/marketplace.json`:

```json
"metadata": {
  "description": "MLX optimization plugin marketplace for GitHub Copilot CLI and VS Code.",
  "version": "0.2.0"
}
```

and inside `plugins[0]`:

```json
"version": "0.2.0"
```

- [ ] **Step 7: Bump Codex manifest**

Modify `plugins/mlx-optimizer/.codex-plugin/plugin.json`:

```json
"version": "0.2.0"
```

- [ ] **Step 8: Run packaging tests**

Run:

```bash
.venv/bin/python -m unittest tests.test_mlx_tools.PluginPackagingTests -v
```

Expected: all `PluginPackagingTests` pass.

- [ ] **Step 9: Validate all JSON manifests**

Run:

```bash
.venv/bin/python -m json.tool plugin.json >/dev/null
.venv/bin/python -m json.tool .github/plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .agents/plugins/marketplace.json >/dev/null
.venv/bin/python -m json.tool .claude-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .cursor-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.codex-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.claude-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.cursor-plugin/plugin.json >/dev/null
```

Expected: all commands exit `0`.

- [ ] **Step 10: Commit manifest support**

Run:

```bash
git add plugin.json .github/plugin/marketplace.json plugins/mlx-optimizer/.codex-plugin/plugin.json .claude-plugin/marketplace.json .cursor-plugin/marketplace.json plugins/mlx-optimizer/.claude-plugin/plugin.json plugins/mlx-optimizer/.cursor-plugin/plugin.json
git diff --cached --check
git commit -m "feat: add Claude and Cursor plugin manifests"
```

Expected: commit succeeds with only manifest files staged.

## Task 3: Documentation, Issue Templates, and CI

**Files:**
- Modify: `README.md`
- Modify: `.github/copilot-instructions.md`
- Modify: `.github/ISSUE_TEMPLATE/bug_report.md`
- Modify: `.github/ISSUE_TEMPLATE/feature_request.md`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Update README supported surfaces**

In `README.md`, replace the supported surfaces table with:

```markdown
| Surface | Files | Install selector |
| --- | --- | --- |
| Codex | `plugins/mlx-optimizer/.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` | `mlx-optimizer@mlx-optimizer-local` |
| GitHub Copilot CLI / VS Code Agent Plugins | `plugin.json` and `.github/plugin/marketplace.json` | `mlx-optimizer@mlx-optimizer` |
| Claude Code | `plugins/mlx-optimizer/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` | `mlx-optimizer@mlx-optimizer` |
| Cursor | `plugins/mlx-optimizer/.cursor-plugin/plugin.json` and `.cursor-plugin/marketplace.json` | Local/team marketplace plugin |
```

Replace the paragraph below the table with:

```markdown
The canonical plugin implementation lives in `plugins/mlx-optimizer/`. The root
`plugin.json` exists so Copilot and VS Code can resolve the same skill bundle
from the repository root. Claude Code and Cursor use tool-specific manifests
inside the canonical plugin root and marketplace files at the repository root.
```

- [ ] **Step 2: Add Claude Code README install section**

Insert this section after the GitHub Copilot CLI section:

````markdown
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
````

- [ ] **Step 3: Add Cursor README install section**

Insert this section after the VS Code Agent Plugins section:

````markdown
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
````

- [ ] **Step 4: Update README repository layout**

In the README layout block, add:

```text
├── .claude-plugin/marketplace.json
├── .cursor-plugin/marketplace.json
```

and under `plugins/mlx-optimizer/`, add:

```text
│   ├── .claude-plugin/plugin.json
│   ├── .cursor-plugin/plugin.json
```

- [ ] **Step 5: Update README validation commands**

In the README validation block, add:

```bash
.venv/bin/python -m json.tool .claude-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .cursor-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.claude-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.cursor-plugin/plugin.json >/dev/null
```

In the release checklist, include:

```markdown
- `.claude-plugin/marketplace.json`
- `.cursor-plugin/marketplace.json`
- `plugins/mlx-optimizer/.claude-plugin/plugin.json`
- `plugins/mlx-optimizer/.cursor-plugin/plugin.json`
```

- [ ] **Step 6: Update Copilot instructions overview and validation**

Modify `.github/copilot-instructions.md` overview sentence to:

```markdown
This repository packages `mlx-optimizer`, a Python-first MLX optimization plugin
for Apple Silicon. It targets Codex, GitHub Copilot CLI, VS Code Agent Plugins,
Claude Code, and Cursor.
```

Modify the canonical implementation paragraph to:

```markdown
The canonical plugin implementation is in `plugins/mlx-optimizer/`. Root-level
metadata exists for Copilot/VS Code packaging, and tool-specific marketplace
files exist for Codex, Claude Code, and Cursor.
```

Add these validation commands to the build/test block:

```bash
.venv/bin/python -m json.tool .claude-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .cursor-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.claude-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.cursor-plugin/plugin.json >/dev/null
```

In project layout, add:

```text
.claude-plugin/marketplace.json                 Claude Code marketplace entry
.cursor-plugin/marketplace.json                 Cursor marketplace entry
plugins/mlx-optimizer/.claude-plugin/plugin.json Claude Code plugin manifest
plugins/mlx-optimizer/.cursor-plugin/plugin.json Cursor plugin manifest
```

Replace the packaging convention bullet with:

```markdown
- Preserve the packaging layers: Codex uses `plugins/mlx-optimizer/` plus
  `.agents/plugins/marketplace.json`; Copilot/VS Code uses root `plugin.json`
  plus `.github/plugin/marketplace.json`; Claude Code uses
  `plugins/mlx-optimizer/.claude-plugin/plugin.json` plus
  `.claude-plugin/marketplace.json`; Cursor uses
  `plugins/mlx-optimizer/.cursor-plugin/plugin.json` plus
  `.cursor-plugin/marketplace.json`.
```

- [ ] **Step 7: Update issue templates**

In `.github/ISSUE_TEMPLATE/bug_report.md`, add these affected areas after the VS Code line:

```markdown
- [ ] Claude Code install or runtime
- [ ] Cursor install or runtime
```

In the environment section, replace:

```markdown
- GitHub Copilot CLI or VS Code version, if relevant:
```

with:

```markdown
- GitHub Copilot CLI, VS Code, Claude Code, or Cursor version, if relevant:
```

In `.github/ISSUE_TEMPLATE/feature_request.md`, add these target surfaces after VS Code:

```markdown
- [ ] Claude Code
- [ ] Cursor
```

- [ ] **Step 8: Update CI manifest validation**

In `.github/workflows/ci.yml`, add these lines to the `Validate JSON manifests` step:

```yaml
          python -m json.tool .claude-plugin/marketplace.json >/dev/null
          python -m json.tool .cursor-plugin/marketplace.json >/dev/null
          python -m json.tool plugins/mlx-optimizer/.claude-plugin/plugin.json >/dev/null
          python -m json.tool plugins/mlx-optimizer/.cursor-plugin/plugin.json >/dev/null
```

- [ ] **Step 9: Run focused docs/CI validation**

Run:

```bash
.venv/bin/python -m unittest tests.test_mlx_tools.PluginPackagingTests -v
rg -n ".claude-plugin|.cursor-plugin" README.md .github/copilot-instructions.md .github/workflows/ci.yml
```

Expected: packaging tests pass, and `rg` shows the new Claude/Cursor manifest
paths in docs and CI.

- [ ] **Step 10: Commit docs and CI updates**

Run:

```bash
git add README.md .github/copilot-instructions.md .github/ISSUE_TEMPLATE/bug_report.md .github/ISSUE_TEMPLATE/feature_request.md .github/workflows/ci.yml
git diff --cached --check
git commit -m "docs: document Claude and Cursor plugin support"
```

Expected: commit succeeds with docs, issue templates, and CI workflow staged.

## Task 4: Full Verification and Optional Tool Smoke Checks

**Files:**
- No required file edits.

- [ ] **Step 1: Run full unit tests**

Run:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 2: Compile scripts**

Run:

```bash
.venv/bin/python -m py_compile plugins/mlx-optimizer/scripts/*.py
```

Expected: command exits `0`.

- [ ] **Step 3: Validate all JSON manifests**

Run:

```bash
.venv/bin/python -m json.tool plugin.json >/dev/null
.venv/bin/python -m json.tool .github/plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .agents/plugins/marketplace.json >/dev/null
.venv/bin/python -m json.tool .claude-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool .cursor-plugin/marketplace.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.codex-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.claude-plugin/plugin.json >/dev/null
.venv/bin/python -m json.tool plugins/mlx-optimizer/.cursor-plugin/plugin.json >/dev/null
```

Expected: all commands exit `0`.

- [ ] **Step 4: Run Codex plugin validator when available**

Run:

```bash
if [ -f "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" ]; then
  .venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/mlx-optimizer
fi
```

Expected: validator passes or command is skipped because the validator is absent.

- [ ] **Step 5: Run skill validators when available**

Run:

```bash
if [ -f "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" ]; then
  for skill in plugins/mlx-optimizer/skills/*; do
    .venv/bin/python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
  done
fi
```

Expected: every skill validator invocation passes or command is skipped because the validator is absent.

- [ ] **Step 6: Run Claude validator when available**

Run:

```bash
if command -v claude >/dev/null 2>&1; then
  claude plugin validate /path/to/mlx-optimizer-plugin
  claude plugin validate /path/to/mlx-optimizer-plugin/plugins/mlx-optimizer
fi
```

Expected: Claude validation passes or command is skipped because `claude` is absent.

- [ ] **Step 7: Record Cursor residual risk**

Cursor does not expose a repo-local validator in the reviewed docs. Record this residual risk in the final handoff:

```text
Cursor support was verified by JSON syntax checks and path-resolution tests. Manual Cursor UI smoke install remains optional because no repo-local Cursor plugin validator was available in the reviewed docs.
```

- [ ] **Step 8: Check git state**

Run:

```bash
git status --short --branch
```

Expected: no unstaged or untracked changes remain except any intentionally excluded local files.

- [ ] **Step 9: Final handoff**

Final response must include:

```text
Changed: Claude Code and Cursor manifests/marketplaces, version bump to 0.2.0, packaging tests, README/Copilot instructions, issue templates, CI manifest validation.
Verified: list exact commands and outcomes from Steps 1-6.
Residual risk: Cursor manual UI smoke install not run unless it was actually run.
Commits: list hashes and Conventional Commit subjects created during implementation.
```
