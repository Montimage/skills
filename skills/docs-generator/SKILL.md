---
name: docs-generator
description: "Generate project documentation structure and practical guides. Use when organizing READMEs or adding API docs. Don't use for code changes, CI setup, or branch management."
license: Apache-2.0
effort: medium
metadata:
  version: 1.4.1
  author: Montimage
---

# Documentation Generator

Restructure project documentation for clarity and accessibility.

## When to Use

Use this skill when the user requests a clearer README, organized project docs, API references, architecture diagrams, or contributor guidance. Select only the documentation files relevant to the detected project type.

## Prerequisites

- Work in a git repository with a configured `origin` remote and a clean or safely stashed working tree.
- Identify the project's entry point, package manifest, test command, and existing documentation before drafting.
- Have write access to the target documentation paths; do not assume generated docs may replace source-authored content.

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
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/docs-generator`

### 1. Analyze Project

Scan the project to understand its shape.

**Use sub-agents for parallel discovery.** Launch multiple Agent tool calls concurrently to keep the main context clean:

- **Agent 1 — Stack detection**: Scan for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, and identify the project type (library, API, web app, CLI, microservices), architecture (monorepo, multi-package, single module), and primary language(s). Return a structured summary.
- **Agent 2 — Existing docs inventory**: List all existing documentation files (README.md, docs/, CONTRIBUTING.md, CHANGELOG.md, etc.) and summarize their current state — present, missing, or outdated. Return a checklist.
- **Agent 3 — User personas & project purpose**: Read the main entry point, existing README, and any project description fields to determine the project's purpose, key features, and target user personas (end users, developers, operators). Return a short summary.

Collect the results from all three agents before proceeding.

### 2. Restructure Documentation

**Use sub-agents for parallel file creation.** The documentation targets below are independent of each other. Dispatch them concurrently using the Agent tool, then collect results:

- **Agent A — Root README.md**: Streamline as the project's front door using the project summary from Step 1. Include:
  - Project name + one-line description
  - Badges (build status, version, license)
  - Key features (bullet list, 3-5 items)
  - Quickstart (install + first use in < 5 min)
  - Modules/components summary with links
  - Contributing link + License
- **Agent B — Component READMEs**: Add per module/package/service documentation using the architecture info from Step 1. Include:
  - Purpose and responsibilities
  - Setup instructions specific to the component
  - Testing commands
- **Agent C — docs/ directory**: Create only the files that are relevant to the project type identified in Step 1. Target structure:
  ```
  docs/
  ├── architecture.md      # System design, component diagrams
  ├── api-reference.md     # Endpoints, authentication, examples
  ├── database.md          # Schema, migrations, ER diagrams
  ├── deployment.md        # Production setup, infrastructure
  ├── development.md       # Local setup, contribution workflow
  ├── troubleshooting.md   # Common issues and solutions
  └── user-guide.md        # End-user documentation
  ```

Each agent should return the path(s) of files it created or updated.

Not every project needs all of these. A CLI tool likely needs a user-guide but not an api-reference. A library needs api-reference but not deployment. Use judgment.

### 3. Create Diagrams

Use Mermaid for visual documentation embedded directly in markdown:
- **Architecture diagrams**: Show components and their relationships
- **Data flow diagrams**: Show how data moves through the system
- **Database schemas**: ER diagrams for relational models

Example:

    ```mermaid
    graph TD
        A["Client"] --> B["API Gateway"]
        B --> C["Auth Service"]
        B --> D["Core Service"]
        D --> E["Database"]
    ```

## Example

Input: `Document this CLI for new users.`

Expected output: a concise root README with a working quickstart, links to relevant `docs/` pages, one Mermaid architecture or data-flow diagram where useful, and no invented commands or components.

## Safety and Failure Handling

- Preserve existing documentation by editing in place and reviewing `git diff` before replacing content.
- Before moving, replacing, or deleting a documentation file, show the planned paths and get explicit user confirmation; use a backup or git history when available.
- Never commit or push generated documentation automatically.
- If the project type or source behavior is unclear, stop and ask for clarification rather than inventing API, deployment, or database details.
- If a link or example check fails, report the file and failing reference, correct it, and rerun the validation checklist.

### 4. Validate Documentation

After generating docs, verify:
- [ ] All internal links point to existing files (no broken references)
- [ ] Code examples are accurate and runnable
- [ ] No duplicate information appears across files
- [ ] Heading levels and formatting are consistent
- [ ] Existing content is preserved or the user approved its replacement
- [ ] `git diff --check` exits 0

## Edge Cases

- If no README exists, create one only after confirming the project name, purpose, and first-use command from source files.
- For a monorepo, document each independently usable package and link it from the root README.
- Skip API, database, or deployment pages when the project has no such surface; do not create empty placeholders.
- Treat generated or vendor documentation as read-only unless the user explicitly requests an update.

## Acceptance Criteria

- [ ] Root README has a purpose statement, quickstart, feature summary, module links, contribution guidance, and license information.
- [ ] Every new page has a clear purpose, a valid internal link, and project-specific examples.
- [ ] Mermaid diagrams reflect components found during analysis.
- [ ] Validation results and every changed path are reported.

### Writing Guidelines

- Keep docs concise and scannable — prefer bullet lists and tables over prose
- Adapt structure to project type (skip categories that don't apply)
- Maintain cross-references between related docs
- Remove redundant or outdated content
- Use real examples from the codebase, not generic placeholders
