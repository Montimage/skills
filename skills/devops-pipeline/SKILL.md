---
name: devops-pipeline
effort: medium
description: Implement pre-commit hooks and GitHub Actions for quality assurance. Use when asked to "setup CI/CD", "add pre-commit hooks", "create GitHub Actions", "setup quality gates", "automate testing", "add linting to CI", "setup code quality checks", "configure CI pipeline", "add automated checks", or any DevOps automation for code quality. Detects project type and configures appropriate tools. Trigger this skill whenever the user mentions CI, CD, pre-commit, GitHub Actions, linting automation, or quality gates — even if they don't use those exact terms.
metadata:
  version: 1.2.0
  creator: Montimage
---

# DevOps Pipeline

Implement comprehensive DevOps quality gates adapted to project type.

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

```bash
# Test pre-commit locally
pre-commit run --all-files

# Commit and push to trigger CI
git add .pre-commit-config.yaml .github/workflows/ci.yml
git commit -m "ci: add pre-commit hooks and GitHub Actions"
git push
```

Check GitHub Actions tab for workflow status.

## Tool Selection by Language

| Language | Formatter | Linter | Security | Types |
|----------|-----------|--------|----------|-------|
| JS/TS | Prettier | ESLint | npm audit | TypeScript |
| Python | Black/Ruff | Ruff | Bandit | mypy |
| Go | gofmt | golangci-lint | gosec | built-in |
| Rust | rustfmt | Clippy | cargo-audit | built-in |
| Java | google-java-format | Checkstyle | SpotBugs | - |

## Resources

- [references/precommit-configs.md](references/precommit-configs.md) - Pre-commit configurations by language
- [references/github-actions.md](references/github-actions.md) - GitHub Actions workflow templates
