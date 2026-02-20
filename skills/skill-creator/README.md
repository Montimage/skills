# Skill Creator

> Interactive guide for creating and updating skills that extend Claude's capabilities with specialized workflows.

## Highlights

- Four-phase guided process: Discovery, Approval, Build, Test & Deliver
- Generates SKILL.md with proper frontmatter and progressive disclosure structure
- Creates bundled resources (scripts, references, assets) as needed
- Includes validation, testing, and packaging automation
- Supports updating existing skills with versioned changes

## When to Use

| Say this... | Skill will... |
|---|---|
| "create a new skill" | Guide through Discovery, Approval, Build, and Deliver phases |
| "update this skill" | Read existing skill, propose changes, re-validate and re-package |
| "build a skill for X" | Interactive creation with requirements gathering and approval |
| "package this skill" | Validate and bundle into a distributable .skill file |

## How It Works

```mermaid
graph TD
    A["Discovery"] --> B["Approval"]
    B --> C["Build Skill"]
    C --> D["Test & Deliver"]
    style A fill:#4CAF50,color:#fff
    style D fill:#2196F3,color:#fff
```

## Usage

```
/skill-creator
```

## Output

Creates a complete skill directory with SKILL.md (frontmatter + instructions), README.md, optional scripts/references/assets directories, and a packaged `.skill` file ready for distribution.

## Resources

| Path | Description |
|---|---|
| `scripts/init_skill.py` | Skill directory initializer |
| `scripts/quick_validate.py` | Structural validation script |
| `scripts/package_skill.py` | Skill packaging script |
| `references/workflows.md` | Multi-step workflow design patterns |
| `references/output-patterns.md` | Template and output quality patterns |
