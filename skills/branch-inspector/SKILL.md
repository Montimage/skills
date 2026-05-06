---
name: branch-inspector
description: "Inspect one git branch vs main: overview of commits, diff, merge/PR status, staleness; user picks delete/archive/PR/keep; emit action plan. Use for 'review this branch', 'branch cleanup'. Skip for repo audits, multi-branch sweeps, PR code review."
effort: high
metadata:
  version: 1.1.2
  author: Montimage
---

# Branch Inspector

Inspects a single git branch against `main` to support a cleanup decision. The skill produces a deep overview of what the branch contains, surfaces signals that inform the keep/delete/archive/PR decision, asks the user to choose, then emits a concrete action plan for the chosen path.

## When to use

- The user is cleaning up branches and wants to understand one before acting on it.
- The user names a specific branch ("look at `feature/foo`", "is `experiment/x` worth keeping?").
- The user wants a deep summary of what a branch implements before deciding its fate.

Do **not** use this skill for: scanning many branches at once, full repo audits, or reviewing a PR diff line-by-line.

## Inputs

The branch name is passed as an argument. If the user invokes the skill without one, ask which branch to inspect — do not default to the current branch silently.

The branch may be local (`feature/foo`), remote (`origin/feature/foo`), or both. Detect which exist and report both states.

## Prerequisites

Verify before running. Stop and tell the user if any check fails.

- Current directory is a git repository (`git rev-parse --git-dir` succeeds).
- `main` branch exists locally or on `origin` (`git rev-parse --verify main` or `origin/main`). If the project's primary branch is `master` or something else, ask the user to confirm the comparison base.
- The target branch exists locally or on `origin`. If neither, stop and tell the user.
- `gh` CLI is optional; used to detect linked PRs. If not available, skip the PR-check step rather than failing.

## Repo Sync Before Inspect (mandatory)

Inspection is read-only on the working tree but needs fresh refs to be accurate. Before inspecting:

```bash
git fetch origin --prune
```

`--prune` removes stale remote-tracking refs so the skill doesn't report a branch as "exists on remote" when it was deleted upstream. Do not check out the branch and do not modify the working tree during inspection.

## Workflow

### 1. Resolve the branch

Given the branch name, determine:

- Does it exist locally? (`git rev-parse --verify <branch>`)
- Does it exist on remote? (`git rev-parse --verify origin/<branch>`)
- Are local and remote in sync, or has one diverged from the other?

Pick the inspection target: prefer the local ref if both exist and are in sync, otherwise inspect each side separately and call out the divergence.

### 2. Build the overview

Collect signals across five groups: **identity & activity, merge status, diff scope, implementation depth, staleness**. Run independent git commands in parallel where possible. See `references/overview-fields.md` for the exact field list, the git commands per field, and how to use `git cherry` for squash-merge detection. The implementation-depth group is the one that matters most for the decision — go beyond stats and read the diff to explain what the branch does. If the diff is too large to read in full, spawn an Explore subagent rather than skimming superficially.

### 3. Present the overview

Output a structured report. Use this template:

```
◆ Branch Overview: <branch>
··································································
  Refs:               local=<yes/no> remote=<yes/no> in-sync=<yes/no>
  Tip:                <sha-short> <date> by <author>
  Diverged at:        <sha-short> <date>
  Activity:           <N> commits ahead, <M> commits behind main
                      last commit <X> days ago
  Authors:            <list>
  Diff:               <files> files, +<added>/-<removed> lines
  Top areas:          <dir1>, <dir2>, <dir3>
  Merge status:       <merged | squash-merged | unmerged>
                      cherry-equivalent: <K>/<N> commits already on main
  Linked PR:          <url or "none">
  Conflict risk:      <low | medium | high — files overlap recent main activity>
  Staleness:          <fresh | stale (>30d) | abandoned (>90d)>
  Intent:             <feature | refactor | bugfix | experiment | WIP | unclear>

What this branch implements:
<2-6 sentences describing the actual change, drawn from the diff>

Notable findings:
- <signal 1, e.g., "Adds X module under src/foo, no tests">
- <signal 2, e.g., "Last 3 commits are 'WIP', no rebase since main moved 47 commits">
- <signal 3>

Recommendation: <delete | archive | open PR | keep>
Reasoning: <one sentence>
```

The recommendation is a suggestion, not a decision. Always defer to the user.

### 4. Ask the user to decide

Present four options explicitly:

1. **Delete** — branch is obsolete, already merged, or abandoned with nothing worth saving.
2. **Archive** — preserve the work but get it out of the active branch list.
3. **Open a PR** — branch is ready or close to ready for review.
4. **Keep** — branch is still in active development; no action now.

Ask the user which path to take. Do not act until they answer.

If the user picks **Archive**, follow up with: "Tag-and-delete (`archive/<branch>` tag, then delete branch) or rename to `archive/<branch>`?" Do not assume.

### 5. Emit the action plan

Once the user has decided, output a numbered action plan with the exact commands. Do **not** execute them automatically — this is a cleanup workflow and the user should run the commands themselves or explicitly approve.

See `references/action-plans.md` for the four plan templates (delete, archive tag-and-delete, archive rename, open PR, keep). Pick the template matching the user's decision, substitute `<branch>`, and present the numbered steps to the user. For the PR template, fill in the title and body from the implementation summary built in step 2.

### 6. Stop

The skill emits the plan and stops. Executing destructive commands (`branch -D`, `push --delete`) is the user's call, not the skill's. If the user explicitly asks the skill to run the plan, confirm once before each destructive step.

## Step Completion Reports

Emit a report after the overview phase and after the plan phase.

```
◆ Branch Overview (step 1 of 2 — <branch>)
··································································
  Refs resolved:      √ pass
  Merge status:       √ pass
  Diff analyzed:      √ pass
  Implementation:     √ pass (deep read)
  PR check:           √ pass (or — gh CLI not available)
  ____________________________
  Result:             PASS
```

```
◆ Action Plan (step 2 of 2 — decision: <delete|archive|pr|keep>)
··································································
  Decision captured:  √ pass
  Plan emitted:       √ pass
  Commands listed:    √ pass
  ____________________________
  Result:             PASS
```

## Expected output

A complete run produces three artifacts in the chat, in order:

1. **Branch Overview block** matching the template in step 3 (refs, tip, activity, diff, merge status, linked PR, conflict risk, staleness, intent, "What this branch implements" prose, notable findings, recommendation).
2. **Decision prompt** listing all four options (delete / archive / open PR / keep). For archive, a follow-up prompt asking tag-and-delete vs rename.
3. **Action plan** — the numbered template from `references/action-plans.md` matching the user's choice, with `<branch>` substituted and (for PR) suggested title/body filled in.

See `references/example-output.md` for a worked example showing the overview block, decision prompt, and follow-up plan for an archived branch.

## Acceptance criteria

A run is correct when **all** of these hold:

- The skill ran `git fetch origin --prune` before reading any refs.
- The branch was resolved on both local and remote; divergence (if any) was reported.
- The Overview block contains every field listed in the step 3 template, with no `<placeholder>` left unfilled.
- Merge status was determined using `git cherry main <branch>` (squash-detection), not just `git branch --merged`.
- The "What this branch implements" prose is grounded in the actual diff — it names files, modules, or functions that appear in `git diff main...<branch>`.
- All four decision options were presented; if archive was chosen, the tag-vs-rename follow-up was asked.
- The emitted action plan matches `references/action-plans.md` for the chosen decision, with `<branch>` substituted.
- No destructive command (`branch -D`, `push --delete`, `tag`) was executed by the skill itself.

## Edge cases

- **No `main` branch.** Repos using `master`, `develop`, or `trunk` — ask once and use the answer for the rest of the run.
- **Branch only exists on remote.** Inspect `origin/<branch>` directly; do not check out locally.
- **Branch only exists locally.** Note "remote=no" and skip linked-PR check.
- **Branch is identical to main.** Report 0 commits ahead and recommend delete.
- **Branch is fully squash-merged.** `git branch --merged` says no but `git cherry` shows all `-` lines — recommend delete and call out the squash detection.
- **Diff too large to read in full.** Spawn an Explore subagent to summarize rather than skimming superficially. Note in the overview that the summary is from a subagent.
- **Detached HEAD or invalid name.** Stop and tell the user; do not guess.
- **Active worktree on the branch.** Refuse the delete plan; tell the user to remove the worktree first.
- **`gh` CLI not installed.** Skip the linked-PR check; mark as "n/a — gh not available". Do not fail the run.
- **User refuses to choose.** Print the overview, note "decision deferred", and stop.

## Notes

- **Read-only by default.** The skill never deletes, pushes, or rewrites refs on its own. It emits commands; the user runs them.
- **Don't trust the branch name.** A branch called `fix/typo` may contain a refactor; always verify intent from the diff, not the name.
- **Context budget.** For very large diffs, prefer an Explore subagent over reading the full diff in the main context window — summarized findings cost fewer tokens and keep the overview focused.
