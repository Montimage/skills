# Skill Audit Report: skill-auditor

**Date**: 2026-02-20
**Skill Path**: skills/skill-auditor/
**Auditor**: skill-auditor v1.2.0

## Skill Overview

| Property | Value |
|----------|-------|
| Name | skill-auditor |
| Description | Analyze agent skills for security risks, malicious patterns, and potential dangers before installation. Produces a comprehensive security report with a clear install/reject verdict. |
| Total Files | 4 |
| Script Files | 1 (`scripts/scan_skill.py`) |
| Executable Files | 1 (`scripts/scan_skill.py`) |
| Binary Files | 0 |

## Risk Summary

| Category | Findings | Severity |
|----------|----------|----------|
| Code Execution | 0 | None |
| Network/Exfiltration | 0 | None |
| Filesystem Access | 0 | None |
| Privilege Escalation | 0 | None |
| Obfuscation | 0 | None |
| Prompt Injection | 0 | None |
| Supply Chain | 0 (contextual) | None |
| Credential Exposure | 0 | None |
| Persistence | 0 | None |

**Overall Risk Level**: LOW

## Detailed Findings

### Scanner Pattern Self-Detection (Informational)

The automated scanner reported 178 raw findings. After contextual analysis, **all are false positives** caused by the scanner detecting its own pattern definition strings. This is the expected and unavoidable behavior of a security scanner auditing itself.

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

**File**: `SKILL.md:44-45, 78-79, 288, 317-321`
**Pattern**: npx (package execution), git clone, python -c (safe cleanup)
**Context**: `npx skills add https://github.com/org/repo`, `git clone --depth 1 --single-branch <url> <temp-dir>`, safe cleanup Python one-liner with path validation
**Analysis**: These are documentation strings describing the skill's workflow. `npx` execution requires explicit user confirmation (Phase 4 only). `git clone` uses `--depth 1 --single-branch` for minimal attack surface. Cleanup uses a validated Python command that asserts the path starts with `/tmp/skill-audit-`, has no traversal, and is a directory. All are in the explicit permitted commands allowlist. **Not a risk.**

#### SKILL.md — Prompt Injection Documentation (Informational)

**File**: `SKILL.md:152`
**Pattern**: instruction_manipulation — "override safety"
**Context**: `- Instructions that override safety or hide actions` (in section 1.5 describing what to look for)
**Analysis**: This is an instruction telling the auditor to check for safety override patterns in target files. It is a defensive instruction, not an attack. **Not a risk.**

#### security-checklist.md — Reference Patterns (Informational)

**File**: `references/security-checklist.md:10-92`
**Pattern**: All categories (imports, shell, obfuscation, filesystem, etc.)
**Context**: Checklist entries like `eval()`, `exec()`, `curl | sh`, `~/.ssh/`, etc.
**Analysis**: This is a pure reference document enumerating risk patterns for the auditor to consult. Contains no executable code. All matches are within descriptive text. **Not a risk.**

### Third-Party Content Exposure — W011 (Low)

**File**: `SKILL.md:95-101` (Clone isolation), `SKILL.md:118-127` (Section 1.2)
**Pattern**: Clones arbitrary GitHub repos and reads untrusted files into agent context
**Context**: The skill clones user-specified GitHub repos to audit them. File content is read for analysis.
**Analysis**: This is inherent to the skill's purpose — it must read untrusted code to audit it. Mitigated by:
- Section 1.2 explicitly treats all target files as data, not instructions
- URL validation restricts to `https://github.com/<owner>/<repo>` only
- Clone isolation prevents shell hook execution (no `cd`, `mktemp` unique dirs, absolute paths)
- Permitted commands allowlist prevents executing any target code
**Risk: LOW — mitigated by design.**

### Unverifiable External Dependency — W012 (Low)

**File**: `SKILL.md:83-91` (URL validation), `SKILL.md:317-319` (clone commands)
**Pattern**: Arbitrary GitHub URLs cloned at runtime
**Context**: Users provide GitHub URLs to audit skills before installation.
**Analysis**: The skill validates URLs strictly (no query params, fragments, embedded credentials, or traversal) and uses shallow clones (`--depth 1 --single-branch`). The cloned content is never executed — only scanned and read as data. This is the core value proposition of the skill (audit before install). **Risk: LOW — acceptable for the skill's purpose.**

### Security Hardening Features (Positive Findings)

The skill includes several security-positive features worth noting:

1. **Untrusted content handling** (`SKILL.md:118-127`): Explicit section marking all target files as untrusted input, instructing the agent to never follow instructions found in scanned files.

2. **URL validation** (`SKILL.md:83-91`): Strict GitHub URL validation before cloning — no query params, fragments, embedded credentials, or path traversal.

3. **Clone isolation** (`SKILL.md:93-101`): Unique temp dirs via `mktemp`, no `cd` into cloned repos, absolute paths only.

4. **Credential redaction** (`SKILL.md:169-179`, `scan_skill.py:125-147`): Both the scanner output and report template enforce credential redaction. The `redact_sensitive_context()` function replaces known secret patterns with `[REDACTED]`.

5. **Command allowlist** (`SKILL.md:313-323`): Execution is restricted to exactly 5 commands — the scanner, mktemp, shallow git clone, validated safe cleanup, and user-confirmed installation.

6. **Safe cleanup** (`SKILL.md:320`): Temp directory removal uses Python with assertions (path prefix, no traversal, directory check) instead of raw `rm -rf`.

7. **Read-only scanner** (`scan_skill.py`): The Python scanner only reads files and outputs JSON. It makes no network calls, writes no files, and has no side effects.

8. **Known self-audit findings** (`SKILL.md:303-311`): Transparently documents expected audit findings from self-scanning.

## Files Inventory

| File | Size | Permissions | Executable | Notes |
|------|------|-------------|------------|-------|
| `README.md` | 1,604 B | `-rw-------` | No | Usage documentation — 49 lines |
| `SKILL.md` | 13,586 B | `-rw-------` | No | Main instructions — 323 lines |
| `references/security-checklist.md` | 5,289 B | `-rw-------` | No | Risk taxonomy reference — 145 lines |
| `scripts/scan_skill.py` | 12,332 B | `-rwx------` | Yes | Automated scanner — 335 lines, stdlib only |

## Verdict

### SAFE TO INSTALL

**Reasoning**: The skill-auditor is a read-only security analysis tool. Its only script (`scan_skill.py`) uses exclusively Python standard library modules to scan files and output JSON. All 178 scanner findings are false positives from the scanner detecting its own pattern definitions — an expected and unavoidable artifact. The skill includes strong security hardening: untrusted content boundaries, URL validation, clone isolation, credential redaction, safe cleanup, and a strict command allowlist.

**Minor notes**:
1. W011: Reads untrusted content by design — mitigated by section 1.2 and permitted commands allowlist
2. W012: Clones arbitrary GitHub repos — mitigated by URL validation, shallow clone, and never executing cloned code

**Positive notes**:
1. Prompt injection defenses are present and well-structured (`SKILL.md:118-127`)
2. Credential redaction prevents secret leakage in reports (`scan_skill.py:125-147`)
3. Command execution is restricted to an explicit 5-command allowlist (`SKILL.md:313-323`)
4. Safe cleanup replaces raw `rm -rf` with validated Python deletion (`SKILL.md:320`)
5. Clone isolation prevents shell hook attacks (`SKILL.md:93-101`)
