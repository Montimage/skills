<!--
AI-SKIP: This README is for humans. AI agents reading this skill should
read ../SKILL.md instead — that file is the source of truth for behavior.
-->

# OSS Ready Flow

End-to-end orchestrator that takes a project from its current state to OSS-ready in 6 sequential steps, with one sub-agent per step and a user checkpoint between every step.

## What it does

| Step | Action | Sub-agent | Output |
|------|--------|-----------|--------|
| 1 | Audit current state (wraps `oss-ready` skill) | Auditor (read-only) | `.oss-ready/01-audit.md` |
| 2 | Branch cleanup — classify, plan, per-branch approval | Branch Analyst (read-only) | `.oss-ready/02-branches.md` |
| 3 | Standard docs (user, dev, deployment, architecture) | Docs Architect + Docs Writer | `.oss-ready/03-docs-plan.md`, `.oss-ready/03-docs-diffs.md` |
| 4 | README final polish | README Polisher | `.oss-ready/04-readme-draft.md`, `.oss-ready/04-readme-diff.md` |
| 5 | Related publications collection | Publications Researcher | `.oss-ready/05-publications.md` |
| 6 | Optional GitHub Pages landing page | Landing Page Builder | `.oss-ready/06-landing-page.md` |

## When to use

Trigger phrases: "make this project open source end-to-end", "full OSS prep", "OSS release workflow".

**Don't use for** one-off doc edits, single-file README rewrites, or audit-only checks. For an audit only, use the `oss-ready` skill directly. For just documentation reorganization, use `docs-generator`.

## Safety model

- **Plan-only by default.** Every destructive action (branch delete, history rewrite) requires per-item user approval.
- **No commits without explicit user request.** The skill writes files and shows diffs; the user runs `git commit`.
- **Reports are durable.** Everything lands in `.oss-ready/<step>.md` so the user can resume across sessions.
- **Always ask when ambiguous.** License choice, contact email, branch fate, publication list — no defaults assumed silently.

## How it relates to other skills

- **Wraps:** `oss-ready` (for the step-1 audit). The `oss-ready` skill remains usable on its own.
- **Reuses templates from:** `oss-ready/assets/` (LICENSE, CODE_OF_CONDUCT.md, SECURITY.md, GitHub templates).
- **Coordinates with:** `docs-generator` for step 3 if the user prefers full doc restructuring.

## Restartability

If the user pauses or the session ends, `.oss-ready/` is the source of truth. Re-invoking the skill reads what's there and asks where to resume.

## Files in this skill

- `SKILL.md` — the skill instructions (read by the agent)
- `README.md` — this file
- `evals/evals.json` — minimal smoke test
