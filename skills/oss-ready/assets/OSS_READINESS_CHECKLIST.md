# Open Source Project Checklist

> Concise but comprehensive — everything needed for a clean, professional, contributor-friendly repo.

Track progress here. Mark each item with `[x]` once verified, and add a one-line note pointing to the file, command, or PR that proves it.

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
- [ ] Relevant topics/tags added
- [ ] Repository is **Public**
- [ ] Issues, Discussions, and Projects enabled

## 4. Essential Documentation

- [ ] `README.md` — well-structured with:
  - Project title + tagline
  - Badges (build, version, license, etc.)
  - Features
  - Quick install & usage examples
  - Screenshot/GIF (if applicable)
  - Contribution section
  - License & acknowledgments
- [ ] `CONTRIBUTING.md` — setup instructions, coding standards, PR process
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant recommended)
- [ ] `SECURITY.md` — vulnerability reporting instructions
- [ ] Issue & PR templates (`.github/ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md`)

## 5. Testing & Automation

- [ ] Unit/integration tests exist and pass
- [ ] CI/CD pipeline (GitHub Actions recommended):
  - Lint + test on push/PR
  - Build verification
- [ ] Dependabot enabled for dependency updates
- [ ] Code coverage (optional but strong signal)

## 6. GitHub Settings & Policies

- [ ] Default branch = `main`
- [ ] Branch protection on `main` (require PR review + status checks)
- [ ] Community profile is "Healthy" (license + CoC + templates)
- [ ] Clear issue labels (`good first issue`, `bug`, `enhancement`, etc.)
- [ ] Repository topics and description optimized for discovery

## 7. Packaging & Installation

- [ ] Easy install command in README (e.g. `pip install .`, `npm install`, etc.)
- [ ] Proper package metadata (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.)
- [ ] Published to package registry (PyPI, npm, crates.io, etc.) — if applicable

## 8. Final Polish & Release

- [ ] `CHANGELOG.md` or GitHub Releases with clear versioning
- [ ] Roadmap or future plans visible
- [ ] No broken links or outdated info
- [ ] At least one other maintainer (optional but recommended)
- [ ] First issues welcoming to new contributors

## Bonus "Great" Items (Highly Recommended)

- [ ] Conventional commits
- [ ] Architecture diagram or demo GIF in README
- [ ] Pre-commit hooks
- [ ] Funding file (`FUNDING.yml`) if you want sponsorships

---

## Quick Validation

Visit your repo → **Insights → Community** tab. Aim for all green checks.

Mark everything as done, and your project will give an excellent first impression to users and contributors.
