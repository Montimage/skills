# Action Plan Templates

Use these templates verbatim for the chosen decision. Substitute `<branch>` with the inspected branch name. Never execute the commands automatically — list them for the user.

## Delete

```
1. Verify nothing local depends on the branch (no worktree, no in-progress rebase).
   Command: git worktree list | grep <branch>
2. Delete local ref (force if unmerged and the user confirmed):
   Command: git branch -D <branch>
3. Delete remote ref (if it exists):
   Command: git push origin --delete <branch>
4. Confirm gone:
   Command: git branch -a | grep <branch>   # expect no output
```

## Archive — tag-and-delete (preferred)

```
1. Create archive tag pointing at the branch tip:
   Command: git tag archive/<branch> <branch>
2. Push the tag:
   Command: git push origin archive/<branch>
3. Delete local branch:
   Command: git branch -D <branch>
4. Delete remote branch:
   Command: git push origin --delete <branch>
5. Recovery note: restore with `git checkout -b <branch> archive/<branch>`.
```

## Archive — rename namespace

```
1. Rename local branch:
   Command: git branch -m <branch> archive/<branch>
2. Push renamed branch:
   Command: git push origin archive/<branch>
3. Delete the old remote ref:
   Command: git push origin --delete <branch>
```

## Open a PR

```
1. Push latest if local is ahead of remote:
   Command: git push origin <branch>
2. (Optional) Rebase onto current main to reduce conflicts:
   Command: git fetch origin && git rebase origin/main   # only if user wants this
3. Create PR with summary drawn from the overview:
   Command: gh pr create --base main --head <branch> --title "<title>" --body "<body>"
4. Suggested title: <derived from commits / intent>
   Suggested body: <bullet summary of what the branch implements, taken from the overview>
```

Draft the title and body from the implementation summary built during the overview phase — don't leave the user to write them from scratch.

## Keep

```
No action. Optional follow-ups:
- Rebase on main to stay current: git fetch origin && git rebase origin/main
- Note the next milestone or blocker so future-you remembers why this is open.
```
