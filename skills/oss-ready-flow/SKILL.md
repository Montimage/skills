---
name: oss-ready-flow
description: "Prepare an end-to-end OSS release flow covering audit, branches, docs, README, publications, and optional Pages. Use when coordinating full OSS prep. Don't use for audit-only checks, single-doc edits, or marketing sites."
license: Apache-2.0
effort: high
metadata:
  version: 1.5.4
  author: Montimage
---

# OSS Ready Flow

Orchestrate the full path from a working private/internal project to an OSS-ready public repository. Wraps the existing `oss-ready` audit skill and adds branch cleanup, doc generation, README polish, related-publications collection, and an optional GitHub Pages landing page.

The skill runs 6 steps **sequentially**, with one sub-agent per step so the main conversation stays clean. Every step writes a report to `.oss-ready/<step>.md` in the target repo, returns a structured summary to the main agent, and ends with an explicit user checkpoint before the next step starts.

Destructive actions (branch deletes) are **plan-only by default with per-branch approval**.

## Prerequisites

- `git` and a target repo with at least one commit.
- Authenticated `gh` for GitHub-side checks; if unavailable, mark those checks `n/a` in the report.
- Installed `oss-ready`, write access, and a clean or safely stashed working tree.

If any prerequisite is missing, stop and tell the user; do not silently degrade.

## Dependency Preflight (mandatory)

This skill invokes `oss-ready`. Run this preflight before Repo Sync, stashing, or any target-repo edits. Check the installed dependency's required checklist, not just its name:

```bash
if ! command -v asm >/dev/null 2>&1; then
  echo "Missing required CLI: asm" >&2
  echo "Install it:      npm install -g agent-skill-manager" >&2
  exit 1
fi
installed_skills="$(asm list --json)" || {
  echo "Unable to query installed skills with asm" >&2
  exit 1
}
printf '%s\n' "$installed_skills" | grep -q '"name": "oss-ready"' || {
  echo "Missing required skill: oss-ready" >&2
  echo "Install it:      asm install oss-ready -p claude --yes" >&2
  echo "No asm yet:      npm install -g agent-skill-manager" >&2
  echo "Verify:          asm list --json | grep 'oss-ready'" >&2
  exit 1
}
# Run in a subshell so the EXIT trap cleans the borrow at the end of preflight.
(
  set -e
  BORROWED_PATH=''
  cleanup_borrow() {
    if [ -n "$BORROWED_PATH" ]; then
      asm cleanup "$BORROWED_PATH"
    fi
  }
  trap cleanup_borrow EXIT
  if ! BORROWED_PATH="$(asm get oss-ready --path 2>/dev/null)"; then
    echo "Unable to resolve installed skill: oss-ready; install/update it with asm" >&2
    exit 1
  fi
  if [ -z "$BORROWED_PATH" ] || [ ! -d "$BORROWED_PATH/assets" ] ||
     [ ! -f "$BORROWED_PATH/assets/OSS_READINESS_CHECKLIST.md" ]; then
    echo "Incompatible oss-ready: missing assets/OSS_READINESS_CHECKLIST.md" >&2
    echo "Install/update oss-ready with asm before running this flow" >&2
    exit 1
  fi
) || exit 1
```

Check all installed providers, not only Claude. If `asm` is absent, lookup fails, the skill is missing, or the installed assets are incompatible, stop before touching the target repo. Preserve the exact borrowed path and clean it on success and failure; do not continue with a partial run.

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

- Inspect real files/config; ask when license, branch fate, or publication intent is ambiguous.
- Require per-item approval before deleting, rewriting history, or force-pushing; never commit without an explicit request.
- Keep reports append-only; reruns create `<step>.<run-N>.md`.

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

Dispatch each worker as `general-purpose` (or `Explore` for read-only work) using `references/sub-agent-briefs.md`. Pass its exact `.oss-ready/` output path and prohibited scope; require a summary of 200 words or fewer. The main agent reviews each result, surfaces it to the user, and waits at every action point.

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

Resolve the installed `oss-ready` directory, verify its `assets/`, and copy with its absolute path; never assume a relative sibling path. Read `references/assets-resolution.md` for the required preflight, install instructions, and copy command.

## References

Read `references/sub-agent-briefs.md` for worker contracts, `references/expected-output.md` for report layouts, and `references/edge-cases.md` for recovery. `docs/README.md` is human-facing only.
