# Overview Fields — What to Collect in Step 2

Collect as much signal as the available tools allow. Run independent git commands in parallel where possible.

## Identity & activity

- Tip commit SHA, author, date.
- First commit unique to the branch (where it diverged from main).
- Total commits ahead of main, commits behind main.
- Last activity date and days since.
- All distinct authors who touched the branch.

## Merge status

- Already merged into main? (`git branch --merged main` and `git log main --oneline | grep <sha>`)
- Squash-merged? Check whether the patch-id of branch commits matches any commit on main (`git cherry main <branch>` — lines starting with `-` are equivalent commits already on main).
- Linked PR via `gh pr list --head <branch> --state all --json number,state,title,url` if `gh` is available.

## Diff scope

- Files changed vs main (`git diff --stat main...<branch>`).
- Lines added/removed.
- Top-touched directories.
- File overlap with recent main activity (last 30 days): `git log --since=30.days --name-only --format= main` intersected with the branch's changed files. Rate conflict risk: **low** = 0 overlapping files, **medium** = 1-5, **high** = more than 5 or any file main rewrote (over half its lines changed).

## Implementation depth (the part that matters for the decision)

Go beyond mechanical stats. Read enough of the diff and commit messages to explain *what the branch does*, not just how big it is.

- Read `git log main..<branch>` for commit messages and the story they tell.
- Run `git diff main...<branch>` and inspect the actual changes — which functions/classes/modules were added or modified, what new dependencies were introduced, what tests were added, what was removed.
- For large diffs, read the diff in chunks and prioritize: new files, then modified files in core directories, then test files. Skip vendored/lockfile/generated files.
- Identify the **intent**: feature, refactor, bugfix, experiment, spike, abandoned WIP. Signals: TODO/FIXME density, presence of tests, commit message quality, whether commits look polished or scratch.
- Note unfinished signals: failing-looking commit messages ("WIP", "broken", "trying X"), commented-out code, dangling debug prints.

**Large-diff threshold:** the diff exceeds 2,000 changed lines or 40 files, excluding vendored, lockfile, and generated files. Above it, spawn an Explore subagent to summarize the implementation instead of skimming, and say so on the overview's `Uncertainty:` line. A weak summary is worse than admitting the diff was not read in full.

## Staleness signals

- Days since last commit.
- Has main moved significantly since the branch diverged (commits behind)?
- Are the touched files still present on main, or has the area been rewritten?
