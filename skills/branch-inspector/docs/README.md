# Branch Inspector

> **Note for AI agents:** This README is for humans. If you're an AI agent looking for instructions, read `SKILL.md` in the parent directory instead.

A skill for inspecting a single git branch against `main` during a cleanup process. Produces a deep overview of what the branch contains, surfaces signals (merge status, staleness, conflict risk, implementation intent), helps you decide whether to **delete / archive / open a PR / keep**, and emits a concrete action plan with exact commands.

## What it does

1. Resolves the branch (local, remote, or both) and fetches fresh refs.
2. Builds an overview: identity, activity, merge status, diff scope, implementation summary, staleness.
3. Reads the actual diff to explain *what the branch implements* — not just stats.
4. Recommends a path (delete / archive / PR / keep) with reasoning.
5. Asks you to decide.
6. Emits a numbered action plan with the commands to run.

## Usage

Invoke with the branch name:

```
/branch-inspector feature/some-experiment
```

The skill will not act on the branch — it produces commands you run yourself.

## When to use

- Branch cleanup sessions ("which of these 40 branches can I delete?").
- Returning to an old branch and wondering whether it's worth finishing.
- Deciding whether to turn a long-lived experiment into a PR.

## When not to use

- Reviewing a PR diff line-by-line — use a code-review skill.
- Sweeping all stale branches at once — this skill handles one branch at a time.
- Full repo audits.

## Requirements

- Git repository with a `main` (or equivalent) base branch.
- `gh` CLI is optional; used to detect linked PRs.

## Output

A structured overview followed by a numbered plan. Destructive commands are listed but never executed by the skill.
