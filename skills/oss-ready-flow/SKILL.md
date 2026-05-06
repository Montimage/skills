---
name: oss-ready-flow
description: "Prepare a repository for end-to-end OSS release across 6 sub-agent steps: audit, branch cleanup, docs, README, publications, optional Pages. Use for 'full OSS prep', 'OSS release flow', 'open-source this repo'. Skip for audit-only (use oss-ready) or single-doc edits."
effort: high
license: MIT
metadata:
  version: 1.4.0
  author: Montimage
---

# OSS Ready Flow

Orchestrate the full path from a working private/internal project to an OSS-ready public repository. Wraps the existing `oss-ready` audit skill and adds branch cleanup, doc generation, README polish, related-publications collection, and an optional GitHub Pages landing page.

The skill runs 6 steps **sequentially**, with one sub-agent per step so the main conversation stays clean. Every step writes a report to `.oss-ready/<step>.md` in the target repo, returns a structured summary to the main agent, and ends with an explicit user checkpoint before the next step starts.

Destructive actions (branch deletes) are **plan-only by default with per-branch approval**.

## Prerequisites

- `git` available on PATH; the target is a git repo with at least one commit
- `gh` CLI authenticated (`gh auth status`) for any step that touches GitHub-side state (audit section 6, remote branch deletion, Pages enablement). If missing, those checks degrade to local-only with an explicit `n/a` reason in the report
- The `oss-ready` skill installed (this skill calls into its audit logic and reuses its asset templates)
- Write access to the target repo's working tree
- A clean working tree, or willingness to stash uncommitted changes during Repo Sync

If any prerequisite is missing, stop and tell the user — do not silently degrade.

## Safety Model

This skill performs destructive and visible-to-others actions. Every one is gated:

- **Branch deletes:** plan-only by default. Each delete needs a per-branch "yes, delete <branch>" from the user. Force-delete (`git branch -D`) needs a separate "yes, force-delete <branch>" after seeing the unmerged commits.
- **Force pushes:** never performed. If a step would require one (e.g., history rewrite to drop secrets), the skill stops and hands the command to the user.
- **Commits:** never performed automatically. The skill writes files, stages them, shows the diff. The user runs `git commit`.
- **External web search (step 5):** only after explicit user approval. Default behavior is repo-local scan only.
- **GitHub Pages enablement (step 6):** never enabled remotely. The skill scaffolds files and writes the `gh` commands the user runs themselves.
- **Sub-agent scope:** every sub-agent receives an explicit "do NOT modify X" clause. If a sub-agent edits outside its brief, the main agent reverts (`git checkout -- <file>`) and re-dispatches.
- **Refusal triggers:** target is the skills repo itself (refuse), `origin` missing during Repo Sync (ask, do not skip), branch labelled `protected-do-not-touch` (refuse to touch even on user request without a second confirmation).

## Repo Sync Before Edits (mandatory)

Before making any changes, sync with the remote to avoid conflicts:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty, stash first, sync, then pop. If `origin` is missing or conflicts occur, stop and ask the user before continuing.

## Ground Rules

- **Always base work on the existing codebase.** Sub-agents must inspect actual files, git history, and config before producing any report or edit. No hallucinated stacks, branches, or features.
- **Always ask the user when information is ambiguous.** If a sub-agent can't determine intent (license, branch fate, publication list), surface a question via `AskUserQuestion`.
- **Never delete or force-push without per-item approval.** This applies to branches, history rewrites, and any rebase that drops commits.
- **No commits without an explicit user request.** The skill writes files and stages diffs; the user runs the commit.
- **Reports are append-only within a session.** Re-running a step creates `<step>.<run-N>.md`; prior reports are not overwritten.

## Workflow

### 0. Setup

1. Confirm the working directory is the *target* repo, not the skills repo. If unclear, ask.
2. Run **Repo Sync** (above).
3. Create `.oss-ready/` at the repo root.
4. Ask the user upfront for: license preference (default MIT), primary contact email for SECURITY.md, whether the project has a public GitHub remote yet.

### 1. Audit Current State

Spawn `general-purpose` sub-agent **Auditor**. Brief: see `references/sub-agent-briefs.md` (Step 1).

After the sub-agent returns, emit the Step 1 Step Completion Report (template in `references/expected-output.md`), list `Done` and `To do` items, and ask: "Proceed to Step 2 (branch cleanup)? [yes / skip / stop]". Wait for confirmation.

### 2. Branch Cleanup

**Goal:** end with `main` as the only branch, with all valuable work merged or archived.

Spawn sub-agent **Branch Analyst** (read-only). Brief: `references/sub-agent-briefs.md` (Step 2).

After the report comes back, emit the Step 2 report (template in `references/expected-output.md`). Then for each non-protected branch, ask the user **per branch** with `AskUserQuestion`:

- Merge into main (open PR)
- Delete (local only / local + remote)
- Keep (with reason)
- Skip for now

Execute approved actions one at a time. After each action, append the result to `.oss-ready/02-branches.md`. **Never use `git push --force` or `git branch -D` without an explicit "yes, delete <branch-name>"** from the user.

Action point: "Branch cleanup done. Proceed to Step 3 (docs)? [yes / skip / stop]"

### 3. Docs (Standard Documentation)

Two sub-agents run in sequence:

1. **Docs Architect** produces a plan only (no writes). Brief: `references/sub-agent-briefs.md` (Step 3a). Result lands in `.oss-ready/03-docs-plan.md`.
2. User reviews and approves the plan.
3. **Docs Writer** applies the approved plan and captures diffs. Brief: `references/sub-agent-briefs.md` (Step 3b).

Show each diff to the user before moving on. The user can request revisions inline; re-dispatch the Writer with the revision request.

For LICENSE / CODE_OF_CONDUCT.md / SECURITY.md, the Writer must `cp` from `oss-ready/assets/` rather than read+write — those files contain language that triggers content filtering on read. Use `sed` for placeholder substitution after copying.

Action point: "Docs done. Proceed to Step 4 (README)? [yes / skip / stop]"

### 4. README

Spawn sub-agent **README Polisher**. Brief: `references/sub-agent-briefs.md` (Step 4).

Show the diff to the user. Apply on approval. **Do not commit.**

Action point: "README done. Proceed to Step 5 (related publications)? [yes / skip / stop]"

### 5. Related Publications

Spawn sub-agent **Publications Researcher**. Brief: `references/sub-agent-briefs.md` (Step 5).

The main agent must pause the sub-agent after its baseline repo scan to ask the user for known publications and whether to do an external web search, then resume the sub-agent with that input.

After the sub-agent returns, show the proposed `## Related Publications` README section, apply on approval, and update `.oss-ready/04-readme-diff.md` accordingly.

Action point: "Publications done. Add a landing page (Step 6, optional)? [yes / skip / stop]"

### 6. Optional — GitHub Pages Landing Page

If the user opts in, spawn sub-agent **Landing Page Builder**. Brief: `references/sub-agent-briefs.md` (Step 6).

If declined, mark step 6 as skipped in the final report.

### 7. Final Summary

After all steps (or after the user stops), emit the Final Summary block (template in `references/expected-output.md`). List every file created/modified, open questions the user deferred, manual follow-ups (`gh repo edit --add-topic ...`, "Enable GitHub Pages in repo settings"), and a suggested commit message for the user to run themselves.

## Sub-agent Dispatch Pattern

All sub-agents are spawned with `subagent_type: general-purpose` (or `Explore` for purely read-only audit-style passes) and a self-contained brief from `references/sub-agent-briefs.md`. Each brief specifies: what to read, what to write (exact paths under `.oss-ready/`), what NOT to modify, and what to return (≤ 200 words).

The main agent never duplicates the sub-agent's work. After receiving a summary, the main agent surfaces it to the user, asks the action-point question, and waits.

## Restartability

The skill is restartable. `.oss-ready/` is the source of truth. On re-invocation, the main agent reads `.oss-ready/` first, asks the user where to resume, and continues from that step. New runs append to existing reports as `<step>.<run-N>.md`.

## Acceptance Criteria

The flow is complete when:

- `.oss-ready/01-audit.md` exists with `PASS` or `PARTIAL` status and explicit per-section counts
- All non-protected branches have been reconciled (merged, deleted with user approval, or explicitly kept) — verified by `git branch -a` showing only `main` and user-kept protected branches
- All standard docs from the step-3 plan exist in `docs/` (or are explicitly skipped) and are referenced from the README
- README contains: tagline, install, usage example, link to `docs/`, related publications section, license
- `.oss-ready/05-publications.md` exists with at least the repo-scanned baseline (zero entries is valid if confirmed)
- If step 6 ran: `docs/index.md` (or equivalent) and `_config.yml` are present, and `.oss-ready/06-landing-page.md` documents the Pages enable steps
- The Final Summary in step 7 is emitted with status per step

A run that stops mid-flow is a **partial**, not a failure. Step 7 always runs and labels each step `done | partial | skipped`.

## Expected Output

See `references/expected-output.md` for the full target directory layout, the per-step Step Completion Report templates, and the Final Summary block.

## Edge Cases

See `references/edge-cases.md` for the full list. Key entries: no git remote, partially-OSS repo, user stops mid-step, conflicting branch deletions, huge README diffs, sub-agent scope violations, prior-run reports, target-is-skills-repo.

## Assets

This skill ships no assets of its own. Templates come from the `oss-ready` skill (`/Users/montimage/dev-montimage/skills/skills/oss-ready/assets/`) and from `docs-generator` where applicable.

## References

- `references/sub-agent-briefs.md` — verbatim briefs for every sub-agent
- `references/expected-output.md` — directory layout and report templates
- `references/edge-cases.md` — recovery and refusal patterns
- `docs/README.md` — human-facing overview
