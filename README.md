<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/logo-white.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo/logo-black.svg">
    <img src="assets/logo/logo-black.svg" alt="Montimage Skills" width="400">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Montimage/skills/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/Release-v1.0.0-E5A630.svg" alt="Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
  <a href="#available-skills"><img src="https://img.shields.io/badge/Skills-10-green.svg" alt="Skills"></a>
</p>

A curated collection of Agent Skills by [Montimage](https://www.montimage.com/) that supercharge AI agents with specialized workflows, domain expertise, and reusable tooling for software development tasks. Works with Claude Code, Codex, OpenClaw, and other AI tools that support skill-based workflows.

## What Are Agent Skills?

Agent Skills are modular, self-contained packages that transform AI agents from general-purpose assistants into specialized tools. Each skill provides procedural knowledge, scripts, reference material, and templates for specific development workflows.

## Available Skills

### Code Quality & Testing

| Skill | Description |
|-------|-------------|
| **[code-review](skills/code-review/)** | Review code for smells, security issues, and Pragmatic Programmer violations with severity-based reports |
| **[test-coverage](skills/test-coverage/)** | Identify untested branches, error paths, and edge cases, then generate targeted tests |

### DevOps & Releases

| Skill | Description |
|-------|-------------|
| **[devops-pipeline](skills/devops-pipeline/)** | Auto-detect project stack and configure pre-commit hooks + GitHub Actions CI |
| **[release-notes](skills/release-notes/)** | Generate categorized release notes from git history, merged PRs, and closed issues |

### Documentation & Open Source

| Skill | Description |
|-------|-------------|
| **[docs-generator](skills/docs-generator/)** | Analyze project type and restructure documentation into a coherent hierarchy with diagrams |
| **[oss-ready](skills/oss-ready/)** | Add README, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, and GitHub templates |

### Infrastructure & Optimization

| Skill | Description |
|-------|-------------|
| **[install-script-generator](skills/install-script-generator/)** | Generate cross-platform install scripts with environment detection, verification, and rollback |
| **[ollama-optimizer](skills/ollama-optimizer/)** | Detect hardware (GPU/RAM/CPU), classify tier, and optimize Ollama for maximum performance |

### Skill Development

| Skill | Description |
|-------|-------------|
| **[skill-creator](skills/skill-creator/)** | Guided 4-phase skill creation: Discovery, Approval, Build, Test & Deliver |
| **[skill-auditor](skills/skill-auditor/)** | Scan skills for security risks, prompt injection, and malicious patterns before installation |

## Quick Start

### Installation

Install all skills with a single command:

```bash
npx skills add https://github.com/Montimage/skills
```

Or install a specific skill:

```bash
npx skills add https://github.com/Montimage/skills --skill code-review
npx skills add https://github.com/Montimage/skills --skill oss-ready
```

<p align="center">
  <img src="assets/screenshots/install.png" alt="Installing Montimage Skills" width="600">
</p>

### Usage

Once installed, skills are automatically detected by your AI agent. Simply describe what you need in natural language:

```
# Triggers the code-review skill
> Review my code for smells and quality issues

# Triggers the oss-ready skill
> Make this project open source ready

# Triggers the release-notes skill
> Generate release notes for the latest version
```

## Project Structure

```
skills/
├── skills/                        # All agent skills
│   ├── code-review/               # Code quality reviews
│   ├── devops-pipeline/           # CI/CD and pre-commit setup
│   ├── docs-generator/            # Documentation restructuring
│   ├── install-script-generator/  # Cross-platform installers
│   ├── ollama-optimizer/          # Local LLM optimization
│   ├── oss-ready/                 # Open-source readiness
│   ├── release-notes/             # Changelog generation
│   ├── skill-auditor/             # Security audit for agent skills
│   ├── skill-creator/             # Skill authoring guide
│   └── test-coverage/             # Test coverage expansion
├── assets/                        # Logo and screenshot assets
├── docs/                          # Project documentation
│   ├── ARCHITECTURE.md            # System design and decisions
│   ├── CHANGELOG.md               # Version history
│   ├── DEPLOYMENT.md              # Publishing and distribution
│   └── DEVELOPMENT.md             # Local development setup
├── LICENSE                        # Apache 2.0
├── CONTRIBUTING.md                # Contribution guidelines
├── CODE_OF_CONDUCT.md             # Community standards
└── SECURITY.md                    # Vulnerability reporting
```

## Skill Anatomy

Each skill follows a standard structure:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions for the AI agent
├── README.md         # Required: human-readable documentation
├── scripts/          # Optional: executable code (Python/Bash)
├── references/       # Optional: domain knowledge, documentation
└── assets/           # Optional: templates, icons, fonts
```

The `SKILL.md` file contains YAML frontmatter (`name`, `version`, `description`) that the AI agent reads to determine when to activate the skill, plus markdown instructions loaded on activation. The `README.md` provides human-readable documentation with highlights, trigger phrases, workflow diagrams, and usage instructions.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding new skills
- Improving existing skills
- Reporting bugs and requesting features

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
