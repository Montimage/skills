# Skill Audit Report: skill-auditor

**Date**: 2026-02-19
**Skill Path**: skills/skill-auditor/
**Auditor**: skill-auditor v1.0

## Skill Overview

| Property | Value |
|----------|-------|
| Name | skill-auditor |
| Description | Analyze agent skills for security risks, malicious patterns, and potential dangers before installation. Produces a comprehensive security report with a clear install/reject verdict. |
| Total Files | 3 |
| Script Files | 1 (`scripts/scan_skill.py`) |
| Executable Files | 1 (`scripts/scan_skill.py`) |
| Binary Files | 0 |

## Risk Summary

| Category | Findings | Severity |
|----------|----------|----------|
| Code Execution | 0 real | None |
| Network/Exfiltration | 0 real | None |
| Filesystem Access | 0 real | None |
| Privilege Escalation | 0 real | None |
| Obfuscation | 0 real | None |
| Prompt Injection | 0 real | None |
| Supply Chain | 0 real | None |
| Credential Exposure | 0 real | None |
| Persistence | 0 real | None |

**Overall Risk Level**: LOW

## Detailed Findings

### Scanner Pattern Self-Detection (Informational)

The automated scanner reported 172 raw findings. After contextual analysis, **all are false positives** caused by the scanner detecting its own pattern definition strings. This is the expected and unavoidable behavior of a security scanner auditing itself.

#### scan_skill.py — Pattern Definitions (Informational)

**File**: `scripts/scan_skill.py:25-122`
**Pattern**: dangerous_imports, shell_patterns, obfuscation, sensitive_data, filesystem_access
**Context**: `DANGEROUS_IMPORTS = {"subprocess", "os.system", ...}` and similar pattern definition blocks
**Analysis**: These are string literals inside Python sets and lists that define what the scanner searches for. They are never imported, executed, or used as code. The script's actual imports are limited to `json`, `os`, `re`, `stat`, `sys`, `pathlib` — all standard library, no network or dangerous capabilities. **Not a risk.**

#### scan_skill.py — Redaction Patterns (Informational)

**File**: `scripts/scan_skill.py:125-140`
**Pattern**: sensitive_data (private key reference, AWS credential reference)
**Context**: `REDACTION_PATTERNS` containing regex strings for credential formats
**Analysis**: These are regex patterns used by `redact_sensitive_context()` to replace secrets with `[REDACTED]` in scanner output. They are string patterns, not actual secrets. The redaction function itself is a security improvement. **Not a risk.**

#### SKILL.md — Documentation Examples (Informational)

**File**: `SKILL.md:43-44, 77-78, 253-267, 287-289`
**Pattern**: npx (package execution), git clone, rm -rf
**Context**: `npx skills add https://github.com/org/repo`, `git clone <github-url> /tmp/<repo-name>`, `rm -rf /tmp/<repo-name>`
**Analysis**: These are documentation strings describing the skill's workflow. `npx` execution requires explicit user confirmation (Phase 4 only). `git clone` targets `/tmp/` only. `rm -rf` is scoped to `/tmp/<repo>` cleanup. All are in the explicit permitted commands allowlist. **Not a risk.**

#### SKILL.md — Prompt Injection Documentation (Informational)

**File**: `SKILL.md:131`
**Pattern**: instruction_manipulation — "override safety"
**Context**: `- Instructions that override safety or hide actions` (in section 1.5 describing what to look for)
**Analysis**: This is an instruction telling the auditor to check for safety override patterns in target files. It is a defensive instruction, not an attack. **Not a risk.**

#### security-checklist.md — Reference Patterns (Informational)

**File**: `references/security-checklist.md:10-92`
**Pattern**: All categories (imports, shell, obfuscation, filesystem, etc.)
**Context**: Checklist entries like `eval()`, `exec()`, `curl | sh`, `~/.ssh/`, etc.
**Analysis**: This is a pure reference document enumerating risk patterns for the auditor to consult. Contains no executable code. All matches are within descriptive text. **Not a risk.**

### Security Hardening Features (Positive Findings)

The skill includes several security-positive features worth noting:

1. **Untrusted content handling** (`SKILL.md:97-106`): Explicit section marking all target files as untrusted input, instructing the agent to never follow instructions found in scanned files.

2. **Credential redaction** (`SKILL.md:148-158`, `scan_skill.py:125-147`): Both the scanner output and report template enforce credential redaction. The `redact_sensitive_context()` function replaces known secret patterns (API keys, tokens, passwords, private keys) with `[REDACTED]`.

3. **Command allowlist** (`SKILL.md:282-291`): Execution is restricted to exactly 4 commands — the scanner, git clone, tmp cleanup, and user-confirmed installation. No other commands permitted.

4. **Read-only scanner** (`scan_skill.py`): The Python scanner only reads files and outputs JSON. It makes no network calls, writes no files, and has no side effects.

## Files Inventory

| File | Size | Permissions | Executable | Notes |
|------|------|-------------|------------|-------|
| `SKILL.md` | 11,378 B | `-rw-------` | No | Main instructions — 291 lines |
| `references/security-checklist.md` | 5,289 B | `-rw-------` | No | Risk taxonomy reference — 145 lines |
| `scripts/scan_skill.py` | 12,332 B | `-rwx------` | Yes | Automated scanner — 335 lines, stdlib only |

## Verdict

### SAFE TO INSTALL

**Reasoning**: The skill-auditor is a read-only security analysis tool. Its only script (`scan_skill.py`) uses exclusively Python standard library modules to scan files and output JSON. All 172 scanner findings are false positives from the scanner detecting its own pattern definitions — an expected and unavoidable artifact. The skill includes strong security hardening: untrusted content boundaries, credential redaction, and a strict command allowlist.

**Key concerns**: None identified.

**Positive notes**:
1. Prompt injection defenses are present and well-structured (`SKILL.md:97-106`)
2. Credential redaction prevents secret leakage in reports (`scan_skill.py:125-147`)
3. Command execution is restricted to an explicit 4-command allowlist (`SKILL.md:282-291`)
