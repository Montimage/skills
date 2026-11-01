# Safety Model

Every destructive or visible-to-others action in the flow is gated:

- **Branch deletes:** plan-only by default. Each delete needs a per-branch "yes, delete <branch>" from the user. Force-delete (`git branch -D`) needs a separate "yes, force-delete <branch>" after the user sees the unmerged commits.
- **Force pushes and history rewrites:** never performed. If a step needs one (for example, to drop secrets), stop and hand the command to the user.
- **Commits:** never performed. Write files, stage them, and show the diff; the user runs `git commit`.
- **External web search (Step 5):** only after explicit user approval. The default is a repo-local scan.
- **GitHub Pages (Step 6):** never enabled remotely. Scaffold files and write the `gh` commands for the user.
- **Sub-agent scope:** every brief carries a "do NOT modify X" clause. If a sub-agent edits outside its brief, revert with `git checkout -- <file>` and re-dispatch.
- **Ambiguity:** if license, branch fate, or publication intent is unclear, ask.
- **Refusal triggers:**
  - The target is the skills repo itself: refuse and ask the user to `cd` into the target repo.
  - `origin` is missing during Repo Sync: ask; do not skip the sync silently.
  - A branch is labelled `protected-do-not-touch`: refuse, even on user request, unless the user confirms a second time.
