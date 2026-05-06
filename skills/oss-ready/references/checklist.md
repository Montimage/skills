# Open Source Project Checklist

Full 8-section checklist + bonus items used by Step 5 of `oss-ready`. Each line is binary (done / not done). Capture a one-line justification or pointer (file path, command output, screenshot URL) for each.

## 1. License

- [ ] Choose a standard license (MIT, Apache 2.0, or GPLv3 recommended)
- [ ] Add `LICENSE` file in root (exact license text, no modifications)
- [ ] License is detected by GitHub (shows in repo header) — verify with `gh repo view --json licenseInfo`

## 2. Codebase Cleanup

- [ ] Remove all secrets, keys, passwords, `.env` examples (use `.env.example`)
- [ ] Proper `.gitignore` (language-specific, ignore build artifacts)
- [ ] Consistent code style (linter + formatter run)
- [ ] No unnecessary files (build folders, caches, IDE files)
- [ ] Sensitive history cleaned if needed (`git filter-repo`)

## 3. Repository Setup

- [ ] Clear, descriptive repo name
- [ ] One-sentence description
- [ ] Relevant topics/tags added — verify with `gh repo view --json repositoryTopics`
- [ ] Repository is **Public**
- [ ] Issues, Discussions, and Projects enabled

## 4. Essential Documentation

- [ ] `README.md` — well-structured with: title + tagline, badges, features, install & usage examples, screenshot/GIF, contribution section, license & acknowledgments
- [ ] `CONTRIBUTING.md` — setup, coding standards, PR process
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant recommended)
- [ ] `SECURITY.md` — vulnerability reporting instructions
- [ ] Issue & PR templates (`.github/ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md`)

## 5. Testing & Automation

- [ ] Unit/integration tests exist and pass
- [ ] CI/CD pipeline (GitHub Actions recommended): lint + test on push/PR, build verification
- [ ] Dependabot enabled for dependency updates (`.github/dependabot.yml`)
- [ ] Code coverage reporting (optional but strong signal)

## 6. GitHub Settings & Policies

- [ ] Default branch = `main` — `gh repo view --json defaultBranchRef`
- [ ] Branch protection on `main` (require PR review + status checks) — `gh api repos/{owner}/{repo}/branches/main/protection`
- [ ] Community profile is "Healthy" (license + CoC + templates)
- [ ] Clear issue labels (`good first issue`, `bug`, `enhancement`, etc.)
- [ ] Repository topics and description optimized for discovery

## 7. Packaging & Installation

- [ ] Easy install command in README (e.g. `pip install .`, `npm install`)
- [ ] Proper package metadata (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.)
- [ ] Published to package registry (PyPI, npm, crates.io) — if applicable

## 8. Final Polish & Release

- [ ] CHANGELOG.md or GitHub Releases with clear versioning
- [ ] Roadmap or future plans visible
- [ ] No broken links or outdated info
- [ ] At least one other maintainer (optional)
- [ ] First issues welcoming to new contributors (`good first issue` label populated)

## Bonus "Great" Items

- [ ] Conventional commits
- [ ] Architecture diagram or demo GIF in README
- [ ] Pre-commit hooks (`.pre-commit-config.yaml`)
- [ ] Funding file (`.github/FUNDING.yml`)

## Quick Validation

Direct the maintainer to: **GitHub → Insights → Community Standards** tab. Aim for all green checks.
