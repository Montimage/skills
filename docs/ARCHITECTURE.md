# Architecture

## Overview

Montimage Skills is a collection of modular Claude Code skill packages. Each skill is a self-contained unit that extends Claude's capabilities with specialized workflows and domain knowledge.

## System Design

```
┌─────────────────────────────────────────────┐
│              Claude Code CLI                │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │        Skill Discovery Layer        │    │
│  │  (reads SKILL.md frontmatter)       │    │
│  └──────────┬──────────────────────────┘    │
│             │                               │
│  ┌──────────▼──────────────────────────┐    │
│  │        Skill Activation Layer       │    │
│  │  (loads SKILL.md body on trigger)   │    │
│  └──────────┬──────────────────────────┘    │
│             │                               │
│  ┌──────────▼──────────────────────────┐    │
│  │     Resource Resolution Layer       │    │
│  │  (scripts, references, assets)      │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

1. **Metadata** (always in context) - `name` + `description` from YAML frontmatter (~100 words)
2. **Instructions** (on activation) - SKILL.md body loaded when the skill triggers (<5k words)
3. **Resources** (on demand) - Scripts, references, and assets loaded as needed

## Skill Structure

Each skill follows a standard directory layout:

```
skill-name/
├── SKILL.md          # Required: metadata + workflow instructions
├── scripts/          # Optional: deterministic, reusable code
├── references/       # Optional: domain knowledge loaded into context
└── assets/           # Optional: templates and files used in output
```

## Components

### Skills

| Component | Role |
|-----------|------|
| `code-review` | Static analysis and quality assessment |
| `devops-pipeline` | CI/CD configuration generation |
| `docs-generator` | Documentation structure creation |
| `install-script-generator` | Cross-platform installer scripts |
| `ollama-optimizer` | Hardware-aware LLM configuration |
| `oss-ready` | Open-source readiness preparation |
| `release-notes` | Changelog generation from git history |
| `skill-creator` | Meta-skill for authoring new skills |
| `test-coverage` | Test gap identification and expansion |

### Resource Types

- **Scripts** (`scripts/`): Executable Python/Bash code for deterministic tasks. Token-efficient since they can be executed without loading into context.
- **References** (`references/`): Documentation and domain knowledge. Loaded selectively based on the user's query.
- **Assets** (`assets/`): Templates, icons, and files used in output. Not loaded into context but copied or modified during execution.
