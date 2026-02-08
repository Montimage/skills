# Development Guide

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Git
- Python 3.10+ (for skills with Python scripts)

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Montimage/skills.git
   cd skills
   ```

2. Install a skill locally for testing:
   ```bash
   cp -r skills/<skill-name> ~/.claude/skills/
   ```

## Creating a New Skill

Refer to the [skill-creator](../skills/skill-creator/) skill for a comprehensive guide. The key steps are:

1. Create a directory under `skills/`
2. Write a `SKILL.md` with YAML frontmatter (`name`, `version`, `description`)
3. Add optional `scripts/`, `references/`, and `assets/` directories
4. Test by installing locally and invoking via Claude Code

## Testing Skills

1. Copy the skill to `~/.claude/skills/`
2. Open Claude Code in a test project
3. Invoke the skill with a relevant natural language prompt
4. Verify the output matches expected behavior
5. Iterate on `SKILL.md` and resources as needed

## Debugging

- Check that `SKILL.md` frontmatter is valid YAML
- Ensure the `description` field contains trigger phrases
- Verify scripts are executable (`chmod +x`)
- Test scripts standalone before integrating into the skill

## Code Style

- **SKILL.md**: Use imperative form, keep under 500 lines
- **Python scripts**: Follow PEP 8
- **Markdown**: Use ATX-style headers, fenced code blocks
