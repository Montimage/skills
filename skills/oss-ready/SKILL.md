---
name: oss-ready
version: 1.4.0
description: Transform projects into professional open-source repositories with standard components. Use when users ask to "make this open source", "add open source files", "setup OSS standards", "create contributing guide", "add license", "prepare for public release", "add CODE_OF_CONDUCT", "add SECURITY.md", "GitHub templates", or want to prepare a project for public release with README, CONTRIBUTING, LICENSE, and GitHub templates. Trigger this skill whenever the user mentions open-sourcing, public repos, community standards, or making a project contribution-ready — even if they just say "let's open source this".
author: Montimage
---

# OSS Ready

Transform projects into professional open-source repositories with standard components.

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

```bash
# Copy from the skill's assets directory — use cp, do NOT read+write
SKILL_ASSETS="{SKILL_DIR}/assets"
cp "$SKILL_ASSETS/LICENSE-MIT" LICENSE
cp "$SKILL_ASSETS/CODE_OF_CONDUCT.md" CODE_OF_CONDUCT.md
cp "$SKILL_ASSETS/SECURITY.md" SECURITY.md
```

After copying, only use `sed` to replace placeholders (e.g., `[INSERT CONTACT METHOD]`, `[INSERT EMAIL]`) with project-specific values. Do not rewrite the full file.

### 3. Create GitHub Templates

Copy from the skill's `assets/.github/` using shell commands:

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp "$SKILL_ASSETS/.github/ISSUE_TEMPLATE/bug_report.md" .github/ISSUE_TEMPLATE/
cp "$SKILL_ASSETS/.github/ISSUE_TEMPLATE/feature_request.md" .github/ISSUE_TEMPLATE/
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

### 5. Present Checklist

After completion, show:
- [x] Files created/updated
- [ ] Items needing manual review
- Recommendations for next steps

## Guidelines

- Preserve existing content - enhance, don't replace
- Use professional, welcoming tone
- Adapt to project's actual tech stack
- Include working examples from the actual codebase

## Assets

Templates in `assets/`:
- `LICENSE-MIT` - MIT license template
- `CODE_OF_CONDUCT.md` - Contributor Covenant
- `SECURITY.md` - Security policy template
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
