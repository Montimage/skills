# Security Risk Checklist for Agent Skills

## Risk Categories

### 1. Code Execution Risk (Critical)

Scripts that execute arbitrary code or enable remote code execution.

**Indicators:**
- `eval()`, `exec()`, `compile()` in Python
- `Function()`, `eval()` in JavaScript
- Shell command construction from user input
- Dynamic imports (`__import__`, `importlib`)
- Deserialization of untrusted data (`pickle.load`, `yaml.load` without SafeLoader)

**Severity:** CRITICAL - Can execute arbitrary code on the host machine.

### 2. Network/Exfiltration Risk (Critical)

Code that makes network requests or opens connections.

**Indicators:**
- HTTP libraries (`requests`, `urllib`, `httpx`, `fetch`, `curl`, `wget`)
- Socket operations (`socket`, `paramiko`, `fabric`)
- Cloud SDK usage (`boto3`, `google.cloud`, `azure`)
- Email/FTP (`smtplib`, `ftplib`)
- DNS lookups or `/dev/tcp` access

**Severity:** CRITICAL - Can exfiltrate data, download payloads, or establish C2 channels.

### 3. Filesystem Risk (High)

Code that reads or writes sensitive files or deletes data.

**Indicators:**
- Access to dotfiles (`~/.ssh/`, `~/.aws/`, `~/.env`, `~/.claude/`)
- System file access (`/etc/passwd`, `/etc/shadow`, `/etc/hosts`)
- Recursive deletion (`rm -rf`, `shutil.rmtree`)
- Writing to system directories (`/etc/`, `/usr/`, `/opt/`)
- Writing to home directory dotfiles

**Severity:** HIGH - Can steal credentials, destroy data, or modify system config.

### 4. Privilege Escalation Risk (High)

Code that attempts to gain elevated privileges.

**Indicators:**
- `sudo` usage
- `chmod +s` (setuid)
- `chmod 777` (world-writable)
- Container breakout patterns
- Service management (`systemctl`, `launchctl`, `crontab`)

**Severity:** HIGH - Can gain persistent or elevated access.

### 5. Obfuscation Risk (High)

Code that hides its true intent through encoding or indirection.

**Indicators:**
- Base64 encoded strings (especially decoded at runtime)
- Hex/unicode escape sequences for strings
- Character-by-character string construction
- Dynamic attribute access patterns (`getattr`, `globals()`)
- Minified/obfuscated code that resists reading

**Severity:** HIGH - Obfuscation is a strong indicator of malicious intent in skill context.

### 6. Prompt Injection Risk (High)

SKILL.md or reference files that attempt to manipulate agent behavior.

**Indicators:**
- "Ignore previous instructions"
- "You are now..."
- "Disregard all previous..."
- Fake system messages (`<system>`, `system:`)
- Instructions to hide actions from the user
- Override safety/security restrictions

**Severity:** HIGH - Can hijack agent to perform unauthorized actions.

### 7. Supply Chain Risk (Medium)

Installation of external packages or execution of remote code.

**Indicators:**
- `pip install` / `npm install` of unknown packages
- `git clone` from untrusted sources
- `npx` execution of remote packages
- Download and execute patterns (`curl | sh`, `wget | bash`)

**Severity:** MEDIUM - Can introduce malicious dependencies.

### 8. Credential/Secret Exposure Risk (Medium)

Hardcoded secrets or patterns that access credential stores.

**Indicators:**
- Hardcoded API keys, tokens, passwords
- Access to keychain/keyring
- Reading credential files (`.npmrc`, `.pypirc`, `.aws/credentials`)
- Environment variable manipulation for secrets

**Severity:** MEDIUM - Can leak or steal credentials.

### 9. Persistence Risk (Medium)

Code that establishes persistent access or scheduled tasks.

**Indicators:**
- Crontab modifications
- Systemd/launchd service creation
- Startup script modifications
- Backdoor installation patterns

**Severity:** MEDIUM - Can maintain long-term unauthorized access.

## Verdict Decision Matrix

| Risk Level | Criteria | Verdict |
|------------|----------|---------|
| **SAFE** | No findings, or only informational notes | Install |
| **LOW RISK** | Minor patterns with clear legitimate context (e.g., `subprocess` for PDF conversion) | Install with awareness |
| **MEDIUM RISK** | Network calls, file access, or package installs with plausible legitimate purpose | Review carefully before installing |
| **HIGH RISK** | Obfuscation, credential access, prompt injection, or escalation without clear justification | Do NOT install without thorough manual review |
| **CRITICAL RISK** | Data exfiltration patterns, reverse shells, encoded payloads, or active prompt injection | Do NOT install |

## Contextual Analysis Guidelines

Not every finding is malicious. Apply contextual judgment:

- A PDF skill using `subprocess` to call `pdftk` is expected behavior
- A documentation skill making HTTP requests to fetch API docs may be legitimate
- A deployment skill using `ssh`/`scp` has a valid use case
- An image processing skill importing `PIL`/`tempfile` is normal

**Key questions for contextual analysis:**
1. Does the skill's stated purpose justify the detected patterns?
2. Are network calls targeting known/trusted endpoints or arbitrary URLs?
3. Are filesystem operations scoped to the working directory or reaching into system/home?
4. Is the code readable and its intent clear, or is it obfuscated?
5. Do scripts accept untrusted input that flows into dangerous operations?
6. Are there any patterns that have NO legitimate explanation for this skill type?
