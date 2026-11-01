# Platform-Specific Notes

Read this file during Phase 2 when choosing commands for the detected platform.

## Windows
- Prefer `winget` over `choco` when available
- Use PowerShell for script execution
- If `permissions.is_admin` is false, mark the steps that need admin rights and ask the user to rerun from an elevated PowerShell

## Linux
- Detect distro family (Debian/RedHat/Arch)
- Use the first package manager found in this order: apt, dnf, yum, pacman, zypper
- If `permissions.sudo_available` is false, plan user-level installs or ask the user how to elevate

## macOS
- Use Homebrew as primary package manager
- Use `/opt/homebrew` on Apple Silicon (arm64) and `/usr/local` on Intel (x86_64)
- If Gatekeeper blocks a downloaded binary, stop and ask the user; do not add `xattr` or `spctl` overrides to the plan
