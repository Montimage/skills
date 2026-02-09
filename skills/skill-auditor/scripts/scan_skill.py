#!/usr/bin/env python3
"""
Skill Scanner - Extracts metadata and risk indicators from a skill directory.

Usage:
    scan_skill.py <skill-path>

Outputs JSON with:
- File inventory (name, size, type, permissions)
- Script analysis (shebangs, imports, shell commands, network calls)
- SKILL.md frontmatter and instruction patterns
- Detected risk indicators
"""

import json
import os
import re
import stat
import sys
from pathlib import Path


# --- Risk patterns ---

DANGEROUS_IMPORTS = {
    "subprocess", "os.system", "shutil.rmtree", "ctypes", "socket",
    "http.client", "urllib.request", "urllib3", "requests", "httpx",
    "smtplib", "ftplib", "paramiko", "fabric", "boto3", "google.cloud",
    "azure", "pickle", "marshal", "shelve", "eval", "exec", "compile",
    "importlib", "runpy", "__import__", "webbrowser", "tempfile",
}

DANGEROUS_SHELL_PATTERNS = [
    (r"curl\s+", "curl (network request)"),
    (r"wget\s+", "wget (network download)"),
    (r"rm\s+-rf", "rm -rf (recursive force delete)"),
    (r"rm\s+-r\s", "rm -r (recursive delete)"),
    (r"chmod\s+777", "chmod 777 (world-writable)"),
    (r"chmod\s+\+s", "chmod +s (setuid)"),
    (r"eval\s+", "eval (arbitrary code execution)"),
    (r"base64\s+(-d|--decode)", "base64 decode (obfuscation)"),
    (r"nc\s+(-l|--listen)", "netcat listen (reverse shell indicator)"),
    (r"ncat\s+", "ncat (network utility)"),
    (r"python3?\s+-c\s", "python -c (inline code execution)"),
    (r"bash\s+-c\s", "bash -c (inline shell execution)"),
    (r"sh\s+-c\s", "sh -c (inline shell execution)"),
    (r"\|\s*sh\b", "pipe to shell"),
    (r"\|\s*bash\b", "pipe to bash"),
    (r">\s*/etc/", "write to /etc (system config)"),
    (r">\s*~/\.", "write to dotfile"),
    (r"ssh\s+", "ssh (remote access)"),
    (r"scp\s+", "scp (remote file copy)"),
    (r"rsync\s+", "rsync (remote sync)"),
    (r"docker\s+run", "docker run (container execution)"),
    (r"sudo\s+", "sudo (privilege escalation)"),
    (r"pip\s+install", "pip install (package installation)"),
    (r"npm\s+install", "npm install (package installation)"),
    (r"npx\s+", "npx (package execution)"),
    (r"git\s+clone", "git clone (remote repo download)"),
    (r"git\s+push", "git push (remote repo write)"),
    (r"mkfifo", "mkfifo (named pipe, shell indicator)"),
    (r"/dev/tcp/", "/dev/tcp (network connection)"),
    (r"xargs\s+", "xargs (command chaining)"),
    (r"crontab", "crontab (scheduled task)"),
    (r"launchctl", "launchctl (macOS service)"),
    (r"systemctl", "systemctl (Linux service)"),
    (r"env\s+[A-Z_]+=", "environment variable injection"),
    (r"export\s+[A-Z_]+=", "environment variable export"),
]

OBFUSCATION_PATTERNS = [
    (r"\\x[0-9a-fA-F]{2}", "hex escape sequences"),
    (r"\\u[0-9a-fA-F]{4}", "unicode escape sequences"),
    (r"base64", "base64 encoding/decoding"),
    (r"atob|btoa", "JS base64 functions"),
    (r"String\.fromCharCode", "JS char code construction"),
    (r"chr\(\d+\)", "Python char construction"),
    (r"exec\(", "exec() call"),
    (r"eval\(", "eval() call"),
    (r"compile\(", "compile() call"),
    (r"__import__\(", "dynamic import"),
    (r"getattr\(", "dynamic attribute access"),
    (r"globals\(\)|locals\(\)", "scope introspection"),
]

SENSITIVE_DATA_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"][^'\"]+['\"]", "hardcoded API key"),
    (r"(?i)(secret|password|passwd|pwd)\s*[=:]\s*['\"][^'\"]+['\"]", "hardcoded secret/password"),
    (r"(?i)(token)\s*[=:]\s*['\"][^'\"]{10,}['\"]", "hardcoded token"),
    (r"(?i)(aws_access_key|aws_secret)", "AWS credential reference"),
    (r"(?i)(private[_-]?key)", "private key reference"),
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI-style API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"-----BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY-----", "embedded private key"),
]

FILESYSTEM_PATTERNS = [
    (r"~\/\.", "home directory dotfile access"),
    (r"\$HOME\/\.", "home directory dotfile access"),
    (r"/etc/(passwd|shadow|hosts|sudoers)", "sensitive system file access"),
    (r"\.ssh/", "SSH directory access"),
    (r"\.aws/", "AWS config access"),
    (r"\.env\b", ".env file access"),
    (r"\.claude/", "Claude config access"),
    (r"\.git/config", "git config access"),
    (r"\.npmrc", "npm config access"),
    (r"\.pypirc", "PyPI config access"),
    (r"keychain|keyring", "system keychain access"),
]

INSTRUCTION_MANIPULATION_PATTERNS = [
    (r"(?i)ignore\s+(previous|prior|above)\s+(instructions?|prompts?)", "prompt injection: ignore instructions"),
    (r"(?i)you\s+are\s+now\s+", "prompt injection: role override"),
    (r"(?i)disregard\s+(all|any)\s+(previous|prior)", "prompt injection: disregard prior"),
    (r"(?i)new\s+instructions?\s*:", "prompt injection: new instructions"),
    (r"(?i)system\s*:\s*you", "prompt injection: fake system message"),
    (r"(?i)override\s+(safety|security|restrictions)", "prompt injection: safety override"),
    (r"(?i)<\s*system\s*>", "prompt injection: fake system tag"),
    (r"(?i)act\s+as\s+(if|though)\s+you", "prompt injection: behavioral override"),
    (r"(?i)pretend\s+(you|that)", "prompt injection: pretend directive"),
    (r"(?i)do\s+not\s+(mention|reveal|disclose)", "instruction hiding"),
]


def get_file_info(filepath: Path, skill_root: Path) -> dict:
    """Get metadata about a single file."""
    st = filepath.stat()
    rel = str(filepath.relative_to(skill_root))
    perms = stat.filemode(st.st_mode)
    is_exec = os.access(filepath, os.X_OK)

    return {
        "path": rel,
        "size_bytes": st.st_size,
        "permissions": perms,
        "executable": is_exec,
        "extension": filepath.suffix.lower(),
    }


def scan_text_file(filepath: Path) -> dict:
    """Scan a text file for risk patterns."""
    try:
        content = filepath.read_text(errors="replace")
    except Exception:
        return {"error": "could not read file"}

    lines = content.splitlines()
    findings = {
        "line_count": len(lines),
        "dangerous_imports": [],
        "shell_patterns": [],
        "obfuscation": [],
        "sensitive_data": [],
        "filesystem_access": [],
        "instruction_manipulation": [],
    }

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Check imports
        for imp in DANGEROUS_IMPORTS:
            if imp in stripped:
                findings["dangerous_imports"].append({
                    "line": i,
                    "import": imp,
                    "context": stripped[:120],
                })

        # Check shell patterns
        for pattern, desc in DANGEROUS_SHELL_PATTERNS:
            if re.search(pattern, stripped):
                findings["shell_patterns"].append({
                    "line": i,
                    "pattern": desc,
                    "context": stripped[:120],
                })

        # Check obfuscation
        for pattern, desc in OBFUSCATION_PATTERNS:
            if re.search(pattern, stripped):
                findings["obfuscation"].append({
                    "line": i,
                    "pattern": desc,
                    "context": stripped[:120],
                })

        # Check sensitive data
        for pattern, desc in SENSITIVE_DATA_PATTERNS:
            if re.search(pattern, stripped):
                findings["sensitive_data"].append({
                    "line": i,
                    "pattern": desc,
                    "context": stripped[:120],
                })

        # Check filesystem access
        for pattern, desc in FILESYSTEM_PATTERNS:
            if re.search(pattern, stripped):
                findings["filesystem_access"].append({
                    "line": i,
                    "pattern": desc,
                    "context": stripped[:120],
                })

        # Check instruction manipulation
        for pattern, desc in INSTRUCTION_MANIPULATION_PATTERNS:
            if re.search(pattern, stripped):
                findings["instruction_manipulation"].append({
                    "line": i,
                    "pattern": desc,
                    "context": stripped[:120],
                })

    # Remove empty categories
    return {k: v for k, v in findings.items() if v}


def scan_skill(skill_path: str) -> dict:
    """Scan an entire skill directory."""
    root = Path(skill_path).resolve()

    if not root.is_dir():
        return {"error": f"Not a directory: {root}"}

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return {"error": f"No SKILL.md found in {root}"}

    result = {
        "skill_path": str(root),
        "skill_name": root.name,
        "files": [],
        "file_scans": {},
        "summary": {
            "total_files": 0,
            "executable_files": [],
            "script_files": [],
            "binary_files": [],
            "total_risk_findings": 0,
        },
    }

    TEXT_EXTENSIONS = {
        ".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".jsx", ".tsx",
        ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".cfg",
        ".ini", ".conf", ".html", ".css", ".xml", ".csv", ".rb",
        ".go", ".rs", ".java", ".c", ".cpp", ".h", ".hpp", ".pl",
        ".r", ".sql", ".lua", ".php", ".swift", ".kt",
    }

    BINARY_EXTENSIONS = {
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
        ".pdf", ".zip", ".gz", ".tar", ".bz2", ".7z", ".rar",
        ".woff", ".woff2", ".ttf", ".otf", ".eot",
        ".mp3", ".mp4", ".wav", ".avi", ".mov",
        ".exe", ".dll", ".so", ".dylib", ".bin",
        ".pptx", ".docx", ".xlsx", ".xls",
        ".pyc", ".pyo", ".class", ".o",
    }

    for filepath in sorted(root.rglob("*")):
        if filepath.is_dir():
            continue
        if filepath.name.startswith("."):
            continue

        info = get_file_info(filepath, root)
        result["files"].append(info)
        result["summary"]["total_files"] += 1

        if info["executable"]:
            result["summary"]["executable_files"].append(info["path"])

        ext = info["extension"]

        if ext in BINARY_EXTENSIONS:
            result["summary"]["binary_files"].append(info["path"])
            continue

        if ext in {".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".rb", ".pl", ".php"}:
            result["summary"]["script_files"].append(info["path"])

        if ext in TEXT_EXTENSIONS or ext == "":
            scan = scan_text_file(filepath)
            if len(scan) > 1:  # More than just line_count
                result["file_scans"][info["path"]] = scan
                finding_count = sum(
                    len(v) for k, v in scan.items()
                    if isinstance(v, list)
                )
                result["summary"]["total_risk_findings"] += finding_count

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: scan_skill.py <skill-path>")
        print("\nScans a skill directory for security risk indicators.")
        print("Outputs JSON to stdout.")
        sys.exit(1)

    result = scan_skill(sys.argv[1])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
