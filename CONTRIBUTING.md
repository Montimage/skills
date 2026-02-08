# Contributing to Montimage Skills

Thank you for your interest in contributing! This guide will help you get started.

## How to Contribute

### Reporting Bugs

1. Check existing [issues](https://github.com/Montimage/skills/issues) to avoid duplicates
2. Open a new issue using the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
3. Include clear reproduction steps and environment details

### Suggesting Features

1. Open a new issue using the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
2. Describe the use case and expected behavior

### Submitting Changes

1. Fork the repository
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. Make your changes
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: add new skill for X
   fix: correct typo in skill-creator SKILL.md
   docs: update README with new skill entry
   ```
5. Push to your fork and open a Pull Request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Montimage/skills.git
   cd skills
   ```

2. Install skills locally for testing:
   ```bash
   cp -r skills/<skill-name> ~/.claude/skills/
   ```

3. Test the skill by invoking it in Claude Code with a relevant prompt.

## Adding a New Skill

1. Create a new directory under `skills/`:
   ```
   skills/your-skill-name/
   ├── SKILL.md           # Required
   ├── scripts/           # Optional
   ├── references/        # Optional
   └── assets/            # Optional
   ```

2. Write `SKILL.md` with proper YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   version: 1.0.0
   description: Clear description of what the skill does and when to use it.
   ---
   ```

3. Follow the [skill-creator](skills/skill-creator/) guide for best practices on skill design.

4. Update the README.md skills table with your new skill.

## Branching Strategy

- `main` - stable release branch
- `feat/*` - feature branches
- `fix/*` - bug fix branches
- `docs/*` - documentation changes

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - new feature or skill
- `fix:` - bug fix
- `docs:` - documentation only
- `refactor:` - code restructuring
- `chore:` - maintenance tasks

## Pull Request Process

1. Fill out the PR template completely
2. Ensure your skill follows the standard structure
3. Test your skill with Claude Code before submitting
4. Wait for review - maintainers will respond within a few days

## Coding Standards

- Keep `SKILL.md` files concise (under 500 lines)
- Use imperative form in instructions
- Include working examples from actual usage
- Scripts should be tested and documented
- Follow the progressive disclosure pattern for large skills

## Questions?

Open an issue or start a discussion - we're happy to help!
