# Discovery agent briefs (Step 1)

Hand each brief to one Agent tool call. Run the three concurrently and collect all results before Step 2.

## Agent 1 — Stack detection

Scan for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `*.csproj` and identify the primary language(s), frameworks (React, Next.js, Django, FastAPI, etc.), and build tools (npm, yarn, pnpm, pip, poetry, cargo, go, maven, gradle). Also note any declared runtime versions (`engines`, `requires-python`, `rust-version`, `go` directive) for the CI matrix decision. Return a structured summary.

## Agent 2 — Existing tooling inventory

Check for existing linter/formatter configs (`.eslintrc*`, `.prettierrc*`, `tsconfig.json`, `mypy.ini`, `setup.cfg`, `ruff.toml`) and existing CI configs (`.pre-commit-config.yaml`, `.github/workflows/*.yml`). Return a checklist of what is present vs missing.

## Agent 3 — Repository conventions

Inspect the repo for branch naming conventions, commit message style, and any existing contribution guidelines. Return the conventions found.
