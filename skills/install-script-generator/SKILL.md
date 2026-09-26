---
name: install-script-generator
description: "Generate cross-platform install scripts with environment detection, verification, rollback, and docs. Use when automating installs across Windows, Linux, or macOS. Don't use for feature code, CI setup, or docs-only requests."
license: Apache-2.0
effort: high
metadata:
  version: 1.3.1
  author: Montimage
---

# Install Script Generator

Generate robust, cross-platform installation scripts with automatic environment detection, verification, and documentation.

## Repo Sync Before Edits (mandatory)

Before generating any output files, sync with the remote to avoid conflicts:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty, stash first, sync, then pop. If `origin` is missing or conflicts occur, stop and ask the user before continuing.

## Workflow

### Phase 1: Environment Exploration

Gather comprehensive system information:

```bash
# Run the environment explorer script
python3 {SKILL_DIR}/scripts/env_explorer.py
```

**Use sub-agents for parallel discovery.** Launch multiple Agent tool calls concurrently to keep the main context clean:

- **Agent 1 — System detection**: Run `env_explorer.py` and parse the JSON output. Detect OS, version, CPU architecture, and user permissions (admin/sudo availability). Return a structured summary.
- **Agent 2 — Package manager inventory**: Identify all available package managers (apt, yum, brew, choco, winget) and their versions. Check shell environment (bash, zsh, powershell, cmd). Return a capability list.
- **Agent 3 — Existing dependencies**: Scan for already-installed dependencies and their versions relevant to the target software. Return a dependency status report.

Collect the results from all three agents before proceeding.

The script detects:
- Operating system (Windows/Linux/macOS) and version
- CPU architecture (x86_64, ARM64, etc.)
- Package managers available (apt, yum, brew, choco, winget)
- Shell environment (bash, zsh, powershell, cmd)
- Existing dependencies and versions
- User permissions (admin/sudo availability)

Output: JSON summary of system capabilities and constraints.

### Phase 2: Installation Planning

Based on the environment analysis and target software:

1. **Identify dependencies** - List all required packages/libraries
2. **Check existing installations** - Avoid reinstalling what exists
3. **Order operations** - Resolve dependency graph
4. **Add verification steps** - Each step must be verifiable
5. **Plan rollback** - Define cleanup on failure

Create the plan using:

```bash
python3 {SKILL_DIR}/scripts/plan_generator.py --target "<software_name>" --env-file env_info.json
```

Plan structure:
```yaml
target: "<software_name>"
platform: "detected_os"
steps:
  - name: "Install dependency X"
    command: "..."
    verify: "command to verify success"
    rollback: "cleanup command if failed"
  - name: "Configure system"
    command: "..."
    verify: "..."
```

### Phase 3: Execution

Execute the plan with real-time verification:

```bash
python3 {SKILL_DIR}/scripts/executor.py --plan installation_plan.yaml
```

Execution behavior:
- Run each step sequentially
- Verify success after each step
- On failure: execute rollback, report error, stop
- Log all output for debugging
- Generate installation report

### Phase 4: Documentation Generation

After successful installation, generate usage documentation:

```bash
python3 {SKILL_DIR}/scripts/doc_generator.py --target "<software_name>" --plan installation_plan.yaml
```

**Use sub-agents for parallel documentation.** The documentation sections are independent of each other. Dispatch them concurrently using the Agent tool, then collect results:

- **Agent A — Installation report**: Generate `install_report.md` with the execution log, step-by-step status, and any warnings or errors encountered during installation.
- **Agent B — Usage guide**: Generate `USAGE_GUIDE.md` with a quick start guide, common commands/usage examples, and troubleshooting tips based on the installed software.
- **Agent C — Uninstall & maintenance**: Generate the uninstallation instructions and maintenance notes (upgrade paths, configuration locations, log file paths).

Each agent should return the path(s) of files it created or updated.

Output includes:
- Installation summary (what was installed, where)
- Quick start guide
- Common commands/usage examples
- Troubleshooting tips
- Uninstallation instructions

## Output Files

The skill generates these files in the current directory:

| File | Description |
|------|-------------|
| `env_info.json` | System environment analysis |
| `installation_plan.yaml` | Detailed installation steps |
| `install_report.md` | Execution log and status |
| `USAGE_GUIDE.md` | User documentation |

## Acceptance Criteria

- [ ] `env_info.json` records the detected platform, architecture, package managers, permissions, and paths.
- [ ] `installation_plan.yaml` gives every installation step a command, verification check, and rollback where applicable.
- [ ] Execution verifies each critical step, rolls back on failure, and returns a non-zero status for failed installation.
- [ ] `install_report.md` and `USAGE_GUIDE.md` identify the target, platform, status, and troubleshooting path.
- [ ] Run the generated plan with `--dry-run` before executing package-manager commands.

## Expected Output

A successful run prints a JSON environment summary, writes the plan and reports listed above, and records `SUCCESS` only after all critical verification commands pass. A failed run prints the failing step and rollback result to stderr and exits non-zero.

## Edge Cases

- If no supported package manager is detected, stop with a platform-specific installation question instead of emitting an executable placeholder plan.
- If `env_info.json` or the plan is missing, report the exact path and rerun the preceding phase.
- Treat sudo/admin elevation, shell differences, ARM architectures, and package-manager prompts as explicit plan inputs.

## Platform-Specific Notes

### Windows
- Prefer `winget` over `choco` when available
- Use PowerShell for script execution
- Handle UAC elevation requirements

### Linux
- Detect distro family (Debian/RedHat/Arch)
- Use appropriate package manager
- Handle sudo requirements gracefully

### macOS
- Use Homebrew as primary package manager
- Handle Apple Silicon vs Intel differences
- Respect Gatekeeper and notarization

## Example Usage

User request: "Create an installation script for Node.js"

1. Run env_explorer.py to detect system
2. Generate plan with Node.js as target
3. Execute plan (installs Node.js + npm)
4. Generate USAGE_GUIDE.md with npm commands

## Error Handling

- All scripts exit with non-zero codes on failure
- Verification failures trigger rollback
- Detailed error messages include remediation hints
- Partial installations are cleaned up automatically
