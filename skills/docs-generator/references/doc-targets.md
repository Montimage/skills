# Documentation targets

Loaded by Step 2 and Step 3 of SKILL.md. Use the Step 1 analysis as the only source of facts.

## Root README.md (Agent A)

Streamline the root README as the project's front door. Include:

- Project name + one-line description
- Badges (build status, version, license) — only for services the repo already uses
- Key features (bullet list, 3-5 items)
- Quickstart (install + first use in < 5 min)
- Modules/components summary with links
- Contributing link + License

## Component READMEs (Agent B)

Add one README per module, package, or service. Include:

- Purpose and responsibilities
- Setup instructions specific to the component
- Testing commands

## docs/ directory (Agent C)

Target structure:

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

### Page-selection rule

Create a page only when Step 1 found the surface it documents:

| Page | Create when Step 1 found |
| --- | --- |
| architecture.md | two or more components, packages, or services |
| api-reference.md | a public library API, HTTP/RPC endpoints, or an exported SDK |
| database.md | a schema, migration directory, or ORM models |
| deployment.md | a Dockerfile, IaC, deploy workflow, or hosting config |
| development.md | a build or test command (always true for most repos) |
| troubleshooting.md | known issues in existing docs, issues, or error handling worth explaining |
| user-guide.md | a CLI, UI, or other end-user entry point |

A CLI tool typically gets user-guide but not api-reference. A library gets api-reference but not deployment. If no row matches a page, skip it; never create an empty placeholder.

## Mermaid example (Step 3)

    ```mermaid
    graph TD
        A["Client"] --> B["API Gateway"]
        B --> C["Auth Service"]
        B --> D["Core Service"]
        D --> E["Database"]
    ```

Diagram types: architecture (components and their relationships), data flow (how data moves through the system), and ER diagrams for relational models.

## Writing guidelines

- Keep docs concise and scannable — prefer bullet lists and tables over prose
- Adapt structure to project type (skip categories that don't apply)
- Maintain cross-references between related docs
- Remove redundant or outdated content, after the approval the Safety section requires
- Use real examples from the codebase, not generic placeholders
