# Audit Report Template

Write `SKILL_AUDIT.md` in the current working directory with this structure:

```markdown
# Skill Audit Report: [skill-name]

**Date**: YYYY-MM-DD
**Skill Path**: path/to/skill
**Auditor**: skill-auditor v1.0

## Skill Overview

| Property | Value |
|----------|-------|
| Name | [from frontmatter] |
| Description | [from frontmatter] |
| Total Files | N |
| Script Files | N |
| Executable Files | N |
| Binary Files | N |

## Risk Summary

| Category | Findings | Severity |
|----------|----------|----------|
| Code Execution | N | Critical/High/Medium/Low/None |
| Network/Exfiltration | N | ... |
| Filesystem Access | N | ... |
| Privilege Escalation | N | ... |
| Obfuscation | N | ... |
| Prompt Injection | N | ... |
| Supply Chain | N | ... |
| Credential Exposure | N | ... |
| Persistence | N | ... |

**Overall Risk Level**: [SAFE / LOW / MEDIUM / HIGH / CRITICAL]

## Detailed Findings

### [Category Name] ([Severity])

**File**: `path/to/file:line`
**Pattern**: [what was detected]
**Context**: [quote with secrets redacted as [REDACTED]]
**Analysis**: [whether it is justified and the real risk]

## Files Inventory

[Table of all files with size, permissions, and notes]

## Verdict

### [SAFE TO INSTALL / INSTALL WITH CAUTION / DO NOT INSTALL]

**Reasoning**: [2-3 sentence summary]

**Key concerns** (if any):
1. [Specific concern with file:line reference]
2. [Specific concern with file:line reference]

**Mitigations** (if applicable):
1. [How to reduce the risk]
2. [Files to review or modify]
```

Never include raw API keys, tokens, passwords, or private keys. Redact them as `[REDACTED]`.
