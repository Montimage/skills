---
name: docs-generator
version: 1.3.0
description: Restructure project documentation for clarity and accessibility. Use when users ask to "organize docs", "generate documentation", "improve doc structure", "restructure README", "write docs", "create README", "document my code", "add API docs", "document this project", "help with documentation", or need to reorganize scattered documentation into a coherent structure. Analyzes project type and creates appropriate documentation hierarchy. Trigger this skill whenever the user needs documentation created, reorganized, or improved — even if they just say something like "this project needs docs" or "the README is a mess".
author: Montimage
---

# Documentation Generator

Restructure project documentation for clarity and accessibility.

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

### 4. Quality Checklist

After generating docs, verify:
- [ ] All internal links work (no broken references)
- [ ] Code examples are accurate and runnable
- [ ] No duplicate information across files
- [ ] Consistent formatting and heading levels
- [ ] Existing content preserved (enhanced, not replaced)

### Guidelines

- Keep docs concise and scannable — prefer bullet lists and tables over prose
- Adapt structure to project type (skip categories that don't apply)
- Maintain cross-references between related docs
- Remove redundant or outdated content
- Use real examples from the codebase, not generic placeholders
