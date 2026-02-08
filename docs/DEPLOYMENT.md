# Deployment

## Installation Methods

### Manual Installation

Copy individual skills to the Claude Code skills directory:

```bash
# Single skill
cp -r skills/<skill-name> ~/.claude/skills/

# All skills
cp -r skills/* ~/.claude/skills/
```

### From Repository

```bash
git clone https://github.com/Montimage/skills.git
cp -r skills/skills/* ~/.claude/skills/
```

## Skill Distribution

Skills can be packaged into `.skill` files for distribution using the `skill-creator` skill's packaging script:

```bash
python skills/skill-creator/scripts/package_skill.py skills/<skill-name>
```

This produces a versioned `.skill` file (e.g., `my-skill-1.0.0.skill`) that can be shared.

## Verification

After installation, verify skills are loaded:

1. Open Claude Code
2. Skills with matching descriptions will auto-activate on relevant prompts
3. Test each installed skill with a sample prompt

## Updates

To update skills to the latest version:

```bash
cd skills
git pull origin main
cp -r skills/* ~/.claude/skills/
```
