# Documentation Generator

> Restructure project documentation for clarity and accessibility with appropriate hierarchy for the project type.

## Highlights

- Analyzes project type (library, API, web app, CLI, microservices)
- Streamlines root README.md as an effective entry point
- Creates component-level READMEs per module/package/service
- Generates Mermaid diagrams for architecture and data flow
- Organizes docs/ directory by category

## When to Use

| Say this... | Skill will... |
|---|---|
| "organize docs" | Restructure scattered documentation into coherent hierarchy |
| "generate documentation" | Create docs/ structure with architecture, API, deployment guides |
| "improve doc structure" | Streamline README and add cross-referenced documentation |
| "restructure README" | Refine root README as project entry point with quickstart |

## How It Works

```mermaid
graph TD
    A["Analyze Project Type"] --> B["Restructure Root README"]
    B --> C["Add Component READMEs"]
    C --> D["Organize docs/ Directory"]
    D --> E["Create Mermaid Diagrams"]
    style A fill:#4CAF50,color:#fff
    style E fill:#2196F3,color:#fff
```

## Usage

```
/docs-generator
```

## Output

Creates a structured documentation hierarchy including a streamlined root README.md, component-level READMEs, and a `docs/` directory with architecture, API reference, deployment, development, and troubleshooting guides as applicable.
