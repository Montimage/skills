# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [1.1.0] - 2026-03-13

### Added

- skill-auditor: support GitHub URLs and `npx skills add` commands as input
- skill-auditor: offer installation after safe audit verdicts
- Repo Sync Before Edits guardrail on all 6 repo-mutating skills (code-review, devops-pipeline, docs-generator, oss-ready, release-notes, test-coverage)
- Feature branch creation step for devops-pipeline workflow

### Improved

- All 10 skills: expanded trigger descriptions for better skill activation
- docs-generator: added scan commands, Mermaid examples, quality checklist
- test-coverage: added concrete coverage commands per framework and detection table
- All 10 READMEs updated to match improved skill content

### Fixed

- install-script-generator: multi-line description converted to single-line (required for parser compatibility)
- skill-auditor: hardened against prompt injection, credential leaks, and unrestricted commands
- oss-ready: use `cp` for asset files to avoid content filtering errors
- All skills: fixed missing version fields and H1 titles in READMEs

### Removed

- ollama-optimizer: removed stray generated output file from skill directory

## [1.0.0] - 2026-02-09

### Added

- Initial collection of 9 Agent Skills
  - code-review
  - devops-pipeline
  - docs-generator
  - install-script-generator
  - ollama-optimizer
  - oss-ready
  - release-notes
  - skill-creator
  - test-coverage
- One-command installation via `npx skills add`
- Compatible with Claude Code, Codex, OpenClaw, and other AI tools
- Project documentation: Architecture, Development, Deployment guides
- Open-source readiness: README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- GitHub templates for issues and pull requests
- Theme-aware logo assets (light/dark)

[1.1.0]: https://github.com/Montimage/skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/Montimage/skills/releases/tag/v1.0.0
