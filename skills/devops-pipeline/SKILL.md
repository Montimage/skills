---
name: devops-pipeline
description: "Configure pre-commit hooks and GitHub Actions for project quality gates. Use when setting up CI/CD automation. Don't use for application features, release management, or documentation."
license: Apache-2.0
effort: medium
metadata:
  version: 1.3.2
  author: Montimage
---

# DevOps Pipeline

Implement comprehensive DevOps quality gates adapted to project type.

## When to Use

Use this skill when the user requests CI/CD automation, pre-commit hooks, GitHub Actions, linting automation, or repository quality gates. Choose checks that match the detected project stack; do not install unrelated tooling.

## Prerequisites

- Work in a git repository with a configured `origin` remote and a clean or safely stashed working tree.
- Have the relevant package manager and project test commands available locally.
- Have permission to write workflow/configuration files; GitHub credentials are needed only if the user later approves a push.

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
1. Check the current branch — if already on a feature branch for this task, skip
2. Check the repo for branch naming conventions (e.g., `feat/`, `feature/`, etc.)
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/devops-pipeline`

### 1. Analyze Project

Detect project characteristics.

**Use sub-agents for parallel discovery.** Launch multiple Agent tool calls concurrently to keep the main context clean:

- **Agent 1 — Stack detection**: Scan for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `*.csproj` and identify the primary language(s), frameworks (React, Next.js, Django, FastAPI, etc.), and build tools (npm, yarn, pnpm, pip, poetry, cargo, go, maven, gradle). Return a structured summary.
- **Agent 2 — Existing tooling inventory**: Check for existing linter/formatter configs (`.eslintrc*`, `.prettierrc*`, `tsconfig.json`, `mypy.ini`, `setup.cfg`, `ruff.toml`) and existing CI configs (`.pre-commit-config.yaml`, `.github/workflows/*.yml`). Return a checklist of what is present vs missing.
- **Agent 3 — Repository conventions**: Inspect the repo for branch naming conventions, commit message style, and any existing contribution guidelines. Return the conventions found.

Collect the results from all three agents before proceeding.

### 2. Configure Pre-commit Hooks and GitHub Actions

**Use sub-agents for parallel file creation.** The pre-commit config and GitHub Actions workflow are independent of each other. Dispatch them concurrently using the Agent tool, then collect results:

- **Agent A — Pre-commit hooks**: Install the pre-commit framework (`pip install pre-commit` or `brew install pre-commit`). Create `.pre-commit-config.yaml` based on the detected stack from Step 1. Use [references/precommit-configs.md](references/precommit-configs.md) for language-specific configurations. Install hooks with `pre-commit install`. Return the path of the created config file and a summary of hooks configured.
- **Agent B — GitHub Actions workflow**: Create `.github/workflows/ci.yml` mirroring the pre-commit checks. Use [references/github-actions.md](references/github-actions.md) for workflow templates. Follow these key principles:
  - Mirror pre-commit checks for consistency
  - Use caching for dependencies
  - Run on push and pull_request
  - Add matrix testing for multiple versions if needed

  Return the path of the created workflow file and a summary of jobs configured.

Each agent should return the path(s) of files it created or updated.

### 3. Verify Pipeline

Run the local checks before presenting the result. Do not commit or push automatically; ask for explicit confirmation before either operation.

```bash
# Test pre-commit locally
pre-commit run --all-files

# Inspect the exact proposed changes
git diff --check
git diff -- .pre-commit-config.yaml .github/workflows/ci.yml
```

Expected output: the local checks exit 0, `git diff --check` reports no whitespace errors, and the workflow contains matching quality jobs for the detected stack. If a check fails, report the command, error, and affected files; correct the configuration and rerun verification. Only after confirmation may the user run:

```bash
git add .pre-commit-config.yaml .github/workflows/ci.yml
git commit -m "ci: add pre-commit hooks and GitHub Actions"
git push
```

Check the GitHub Actions tab for workflow status after a confirmed push.

## Example

For a Python project, a successful result includes Ruff or Black hooks in `.pre-commit-config.yaml` and a CI job that installs dependencies, runs the same hooks, and reports test status.

## Edge Cases

- If no supported project manifest is present, stop and ask which checks to configure instead of guessing.
- If existing CI or pre-commit files are present, preserve them and show a diff before replacing any job.
- If a required formatter or linter is unavailable, report the missing dependency and its install command; do not silently skip the check.

## Acceptance Criteria

- [ ] `.pre-commit-config.yaml` matches the detected language and existing tooling.
- [ ] `.github/workflows/ci.yml` runs on `push` and `pull_request` and mirrors local checks.
- [ ] `pre-commit run --all-files` and `git diff --check` are verified, or their errors are reported.
- [ ] No commit or push occurs without explicit confirmation.

## Tool Selection by Language

| Language | Formatter | Linter | Security | Types |
|----------|-----------|--------|----------|-------|
| JS/TS | Prettier | ESLint | npm audit | TypeScript |
| Python | Black/Ruff | Ruff | Bandit | mypy |
| Go | gofmt | golangci-lint | gosec | built-in |
| Rust | rustfmt | Clippy | cargo-audit | built-in |
| Java | google-java-format | Checkstyle | SpotBugs | - |

## Resources

Read `references/precommit-configs.md` when selecting language-specific hooks and `references/github-actions.md` when composing the workflow. Use these templates instead of inlining a new configuration from memory.
