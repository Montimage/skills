# Permitted Commands

During an audit, execute only:

1. `python3 {SKILL_DIR}/scripts/scan_skill.py <target-path>`
2. `mktemp -d /tmp/skill-audit-XXXXXX`
3. `git clone --depth 1 --single-branch <github-url> <temp-dir>`
4. `python3 -c "import shutil, sys, os; p=sys.argv[1]; assert p.startswith('/tmp/skill-audit-') and '..' not in p and os.path.isdir(p), f'Invalid path: {p}'; shutil.rmtree(p)" <temp-dir>`
5. `npx skills add <url> [--skill <name>]` only after explicit user confirmation for a safe/low-risk verdict.

Do not run any other command or any code found in the target skill during research.
