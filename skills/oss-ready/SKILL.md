---
name: oss-ready
effort: high
description: "Add OSS-standard files (README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, GitHub templates) and run an 8-section readiness audit. Use for 'make this open source', 'OSS readiness', 'public release'. Skip for marketing pages or closed code."
metadata:
  version: 1.5.0
  creator: Montimage
---

# OSS Ready

Transform projects into professional open-source repositories with standard components, GitHub templates, and an 8-section OSS readiness audit.

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

**1. License**
- [ ] Choose a standard license (MIT, Apache 2.0, or GPLv3 recommended)
- [ ] Add `LICENSE` file in root (exact license text, no modifications)
- [ ] License is detected by GitHub (shows in repo header) — verify with `gh repo view --json licenseInfo`

**2. Codebase Cleanup**
- [ ] Remove all secrets, keys, passwords, `.env` examples (use `.env.example`)
- [ ] Proper `.gitignore` (language-specific, ignore build artifacts)
- [ ] Consistent code style (linter + formatter run)
- [ ] No unnecessary files (build folders, caches, IDE files)
- [ ] Sensitive history cleaned if needed (`git filter-repo`)

**3. Repository Setup**
- [ ] Clear, descriptive repo name
- [ ] One-sentence description
- [ ] Relevant topics/tags added — verify with `gh repo view --json repositoryTopics`
- [ ] Repository is **Public**
- [ ] Issues, Discussions, and Projects enabled

**4. Essential Documentation**
- [ ] `README.md` — well-structured with: title + tagline, badges, features, install & usage examples, screenshot/GIF, contribution section, license & acknowledgments
- [ ] `CONTRIBUTING.md` — setup, coding standards, PR process
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant recommended)
- [ ] `SECURITY.md` — vulnerability reporting instructions
- [ ] Issue & PR templates (`.github/ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md`)

**5. Testing & Automation**
- [ ] Unit/integration tests exist and pass
- [ ] CI/CD pipeline (GitHub Actions recommended): lint + test on push/PR, build verification
- [ ] Dependabot enabled for dependency updates (`.github/dependabot.yml`)
- [ ] Code coverage reporting (optional but strong signal)

**6. GitHub Settings & Policies**
- [ ] Default branch = `main` — `gh repo view --json defaultBranchRef`
- [ ] Branch protection on `main` (require PR review + status checks) — `gh api repos/{owner}/{repo}/branches/main/protection`
- [ ] Community profile is "Healthy" (license + CoC + templates)
- [ ] Clear issue labels (`good first issue`, `bug`, `enhancement`, etc.)
- [ ] Repository topics and description optimized for discovery

**7. Packaging & Installation**
- [ ] Easy install command in README (e.g. `pip install .`, `npm install`)
- [ ] Proper package metadata (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.)
- [ ] Published to package registry (PyPI, npm, crates.io) — if applicable

**8. Final Polish & Release**
- [ ] CHANGELOG.md or GitHub Releases with clear versioning
- [ ] Roadmap or future plans visible
- [ ] No broken links or outdated info
- [ ] At least one other maintainer (optional)
- [ ] First issues welcoming to new contributors (`good first issue` label populated)

**Bonus "Great" Items**
- [ ] Conventional commits
- [ ] Architecture diagram or demo GIF in README
- [ ] Pre-commit hooks (`.pre-commit-config.yaml`)
- [ ] Funding file (`.github/FUNDING.yml`)

#### Quick Validation

Direct the maintainer to: **GitHub → Insights → Community Standards** tab. Aim for all green checks.

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

## Assets

Templates in `assets/`:
- `LICENSE-MIT` — MIT license template
- `CODE_OF_CONDUCT.md` — Contributor Covenant
- `SECURITY.md` — Security policy template
- `OSS_READINESS_CHECKLIST.md` — Drop-in checklist for the target repo
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
