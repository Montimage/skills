---
name: oss-ready
description: "Add OSS-standard files (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, GitHub templates) and run an 8-section readiness audit. Use for 'make this open source', 'OSS readiness', 'public release'. Skip for marketing pages or closed code."
effort: high
metadata:
  version: 1.8.0
  author: Montimage
---

# OSS Ready

Transform projects into professional open-source repositories with standard components, GitHub templates, and an 8-section OSS readiness audit.

## Prerequisites

Verify before running. Stop and tell the user if any check fails.

- Target directory is a git repository (`git rev-parse --git-dir` succeeds)
- `gh` CLI is installed and authenticated for Section 3 and 6 audits (`gh auth status`)
- Working tree has no unrelated uncommitted edits — run `git status` first; if dirty, ask the user whether to stash or abort
- Skill assets directory is reachable: `test -d "$SKILL_DIR/assets"`
- Write access to the target repo

If `gh` is missing, the audit still runs but Sections 3 and 6 are marked `n/a — gh CLI not available` rather than skipped silently.

## Repo Sync Before Edits (mandatory)

Before making any changes, sync with the remote to avoid conflicts:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty, stash first, sync, then pop. If `origin` is missing or conflicts occur, stop and ask the user before continuing.

## Workflow

### 0. Create Feature Branch

Before making any changes:
1. Check the current branch - if already on a feature branch for this task, skip
2. Check the repo for branch naming conventions (e.g., `feat/`, `feature/`, etc.)
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/oss-ready`

### 1. Analyze Project

Identify:
- Primary language(s) and tech stack
- Project purpose and functionality
- Existing documentation to preserve
- Package manager (npm, pip, cargo, etc.)

**Use sub-agents for parallel discovery.** Launch multiple Agent tool calls concurrently to keep the main context clean:

- **Agent 1 — Stack detection**: Scan for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, and identify the primary language(s), build tools, and package manager. Return a structured summary.
- **Agent 2 — Existing docs inventory**: List all existing documentation files (README, CONTRIBUTING, LICENSE, docs/, .github/) and summarize their current state — present, missing, or outdated. Return a checklist.
- **Agent 3 — Project purpose**: Read the main entry point, existing README, and any project description fields to determine the project's purpose and key features. Return a short project summary.

Collect the results from all three agents before proceeding.

### 2. Create/Update Core Files

**Use sub-agents for parallel file creation.** The files below are independent of each other. Dispatch them concurrently using the Agent tool, then collect results:

- **Agent A — README.md**: Enhance the existing README (or create one) with the sections listed below. Use the project summary from Step 1.
- **Agent B — CONTRIBUTING.md**: Generate the contributing guide with the sections listed below. Use the stack info from Step 1.
- **Agent C — Asset files**: Copy LICENSE, CODE_OF_CONDUCT.md, and SECURITY.md from the skill assets directory using `cp` commands only (never read+write — content triggers filtering). Replace placeholders with `sed` after copying.

Each agent should return the path(s) of files it created or updated.

**README.md** - Enhance with:
- Project overview and motivation
- Key features list
- Quick start (< 5 min setup)
- Prerequisites and installation
- Usage examples with code
- Project structure
- Technology stack
- Contributing link
- License badge

**CONTRIBUTING.md** - Include:
- How to contribute overview
- Development setup
- Branching strategy (feature branches from main)
- Commit conventions (Conventional Commits)
- PR process and review expectations
- Coding standards
- Testing requirements

**LICENSE** - Default to MIT unless specified.

**CODE_OF_CONDUCT.md** - Contributor Covenant.

**SECURITY.md** - Vulnerability reporting process.

**IMPORTANT — Copy asset files using shell commands only.** Some asset files (CODE_OF_CONDUCT.md, SECURITY.md) contain language about harassment, abuse, and vulnerability disclosure that **will trigger content filtering** if you attempt to read and re-write the content. Always use `cp` to copy these files. Never read their contents into context and write them back out.

**Destructive-overwrite caution.** `cp` clobbers existing files silently. Before each copy, check the target with `test -f <path>` — if it exists with non-default content, ask the user before overwriting (`cp -i` will prompt) or back the file up first (`cp <path> <path>.bak`). The audit step (5) is read-only by design; the modification window is steps 2–4 only.

```bash
# Copy from the skill's assets directory — use cp, do NOT read+write
SKILL_ASSETS="{SKILL_DIR}/assets"
for f in LICENSE-MIT:LICENSE CODE_OF_CONDUCT.md:CODE_OF_CONDUCT.md SECURITY.md:SECURITY.md; do
  src="${f%%:*}"; dst="${f##*:}"
  test -f "$dst" && cp "$dst" "$dst.bak"   # backup any existing file
  cp "$SKILL_ASSETS/$src" "$dst"
done
```

After copying, only use `sed` to replace placeholders (e.g., `[INSERT CONTACT METHOD]`, `[INSERT EMAIL]`) with project-specific values. Do not rewrite the full file.

For history rewrites (`git filter-repo` in Step 5 / Section 2): always run with `--dry-run` first, confirm the diff with the user, and require an explicit `git push --force-with-lease` rather than `--force`. Never rewrite history without user confirmation.

### 3. Create GitHub Templates

Copy from the skill's `assets/.github/` using shell commands:

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp "$SKILL_ASSETS/.github/ISSUE_TEMPLATE/bug_report.md" .github/ISSUE_TEMPLATE/
cp "$SKILL_ASSETS/.github/ISSUE_TEMPLATE/feature_request.md" .github/ISSUE_TEMPLATE/
cp "$SKILL_ASSETS/PULL_REQUEST_TEMPLATE.md" .github/ 2>/dev/null || \
  cp "$SKILL_ASSETS/.github/PULL_REQUEST_TEMPLATE.md" .github/
```

### 4. Create Documentation Structure, Metadata, and .gitignore

**Use sub-agents for parallel execution.** These tasks are independent — dispatch them concurrently:

- **Agent D — Documentation structure**: Create the `docs/` directory and populate the relevant files based on the project type identified in Step 1. Target structure:
  ```
  docs/
  ├── ARCHITECTURE.md    # System design, components
  ├── DEVELOPMENT.md     # Dev setup, debugging
  ├── DEPLOYMENT.md      # Production deployment
  └── CHANGELOG.md       # Version history
  ```
- **Agent E — Project metadata**: Update the package file with OSS-standard fields based on the tech stack:
  - **Node.js**: `package.json` — name, description, keywords, repository, license
  - **Python**: `pyproject.toml` or `setup.py`
  - **Rust**: `Cargo.toml`
  - **Go**: `go.mod` + README badges
- **Agent F — .gitignore**: Verify and update `.gitignore` with comprehensive patterns for the detected tech stack.

Each agent should return a summary of what it created or updated.

### 5. OSS Readiness Audit

Run the full **Open Source Project Checklist** against the target repo. Each item is binary (done / not done). For each item, mark the status and capture a one-line justification or pointer (file path, command, screenshot URL, etc.).

**Drop the checklist into the repo** so maintainers can track progress between sessions:

```bash
cp "$SKILL_ASSETS/OSS_READINESS_CHECKLIST.md" docs/OSS_READINESS_CHECKLIST.md
```

**Use sub-agents to run the audit in parallel.** Each section is independent — dispatch concurrently and collect results. The eight sections plus bonus items map to eight + one sub-agents:

- **Audit-1 License**
- **Audit-2 Codebase Cleanup**
- **Audit-3 Repository Setup** (requires `gh` CLI for GitHub-side checks)
- **Audit-4 Essential Documentation**
- **Audit-5 Testing & Automation**
- **Audit-6 GitHub Settings & Policies** (requires `gh` CLI)
- **Audit-7 Packaging & Installation**
- **Audit-8 Final Polish & Release**
- **Audit-Bonus** for the "Great" items

Each audit agent should:
1. Check each checklist item using shell tools (`grep`, `gh`, `ls`, `git`).
2. Return a structured result: `{item, status: done|missing|n/a, evidence}`.
3. Never modify the repo — auditing is read-only here.

#### Open Source Project Checklist

The full checklist (8 sections + bonus items + GitHub Community Standards validation pointer) lives in `references/checklist.md` to keep SKILL.md within the agent's context budget. Each audit sub-agent reads only its assigned section from that file.

```bash
# Copy the drop-in checklist into the target repo so maintainers can track progress
cp "$SKILL_ASSETS/OSS_READINESS_CHECKLIST.md" docs/OSS_READINESS_CHECKLIST.md
```

See `references/checklist.md` for every audit item, the `gh` command that verifies it, and the bonus "Great" items list.

### 6. Present Final Status Report

After steps 1–5, output a Step Completion Report:

```
◆ OSS Readiness (step 6 of 6 — <repo>)
··································································
  Section 1 License:                √ N/3
  Section 2 Codebase Cleanup:       √ N/5
  Section 3 Repository Setup:       √ N/5
  Section 4 Essential Docs:         √ N/5
  Section 5 Testing & Automation:   √ N/4
  Section 6 GitHub Settings:        √ N/5
  Section 7 Packaging:              √ N/3
  Section 8 Final Polish:           √ N/5
  Bonus items:                      √ N/4
  ____________________________
  Result:                           PASS | FAIL | PARTIAL
```

Then list:
- Files created/updated (link each to its path)
- Items still requiring manual action (with the precise remediation step)
- Recommended next commands (`gh repo edit`, `gh api ...`) the user can run themselves

## Guidelines

- Preserve existing content — enhance, don't replace
- Use professional, welcoming tone
- Adapt to project's actual tech stack
- Include working examples from the actual codebase
- Audit before fixing: run Step 5 read-only first, then offer to fix

## Acceptance Criteria

The skill run is complete when **all** of the following are verifiable:

- A feature branch exists and is checked out (or the user explicitly confirmed working on `main`)
- `LICENSE`, `CODE_OF_CONDUCT.md`, `SECURITY.md` exist at the repo root and are byte-identical to the asset templates except for `sed`-replaced placeholders
- `README.md` and `CONTRIBUTING.md` exist and contain every required section listed in Step 2
- `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, and a `PULL_REQUEST_TEMPLATE.md` (root or `.github/`) exist
- `docs/OSS_READINESS_CHECKLIST.md` is present in the target repo
- The audit step (5) was run **read-only** — no files were modified during audit; modifications happen only in steps 1–4
- The Step Completion Report (step 6) emits one line per section with a `done/total` count and a final `PASS | FAIL | PARTIAL` verdict
- No file content sourced from `assets/CODE_OF_CONDUCT.md` or `assets/SECURITY.md` was read into context (only `cp` + `sed` were used) to avoid content filtering on harassment/disclosure language

## Expected Output

The Step Completion Report at the end of the run must match this shape exactly (counts vary per repo):

```
◆ OSS Readiness (step 6 of 6 — my-cool-project)
··································································
  Section 1 License:                √ 3/3
  Section 2 Codebase Cleanup:       √ 4/5
  Section 3 Repository Setup:       √ 5/5
  Section 4 Essential Docs:         √ 5/5
  Section 5 Testing & Automation:   × 2/4
  Section 6 GitHub Settings:        √ 4/5
  Section 7 Packaging:              √ 3/3
  Section 8 Final Polish:           × 2/5
  Bonus items:                      — 1/4
  ____________________________
  Result:                           PARTIAL
```

Followed by:

- **Files created/updated** — each path listed with one line of context
- **Items still requiring manual action** — each with the precise remediation step (e.g., "Enable Dependabot: commit `.github/dependabot.yml` (template available at <url>)")
- **Recommended next commands** — `gh` calls the maintainer can run themselves (e.g., `gh repo edit --add-topic open-source,documentation`)

## Edge Cases

- **Existing files preserved**: if a `LICENSE`, `README.md`, or other root file already exists with non-default content, the skill must enhance, not overwrite. Diff the current file against the asset template; only add missing sections. Ask the user before any destructive replacement.
- **Closed-source / private repo**: when the target repo is private and the user did not explicitly say "make this open source", warn and ask before proceeding — Section 3's "Public" check will always fail, which is expected.
- **Marketing-only repos with no source code**: not in scope. Refuse and route to a docs-site skill.
- **Non-MIT license already chosen**: do not overwrite. Detect existing `LICENSE` headers (Apache 2.0, GPLv3, etc.) and skip the LICENSE copy step; record `done` against Section 1 with the existing license name.
- **Monorepo / multi-package repos**: ask the user which package(s) to target — running the skill at the monorepo root vs. inside a sub-package gives different results. Default to the directory the user invoked from.
- **Asset content filtering**: if any agent attempts to read `CODE_OF_CONDUCT.md` or `SECURITY.md` content into context (vs. `cp`-ing it), the run must abort that sub-task with a clear error and re-issue the copy as a shell command.
- **`gh` not installed**: Sections 3 and 6 emit `n/a — gh CLI not available` for each gh-dependent item; rest of audit proceeds.
- **Dirty working tree at start**: stop and ask before any edit — never auto-stash without confirmation.

## Assets

Templates in `assets/`:
- `LICENSE-MIT` — MIT license template
- `CODE_OF_CONDUCT.md` — Contributor Covenant
- `SECURITY.md` — Security policy template
- `OSS_READINESS_CHECKLIST.md` — Drop-in checklist for the target repo
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
