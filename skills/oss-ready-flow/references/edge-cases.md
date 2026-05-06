# Edge Cases

- **No git remote:** Skip Repo Sync, warn the user, and proceed. Steps that depend on `gh` (audit section 6, branch cleanup remote-side) become local-only; mark the missing checks as `n/a` with a "no remote" reason.
- **Repo already partially OSS-ready:** Audit will show many items `done`. Skip the deterministic asset-copy parts the audit flagged as present; proceed with the remaining steps.
- **User answers "stop" mid-step:** Save the partial state in `.oss-ready/<step>.md`, run step 7 (Final Summary) immediately, and exit. Do not partially-write files outside `.oss-ready/`.
- **Conflicting branch deletions:** If the user approves deleting a branch that has unmerged work, surface the unmerged commits and require a second confirmation. Never use `git branch -D` (force-delete) without "yes, force-delete <branch>".
- **Publications search returns hundreds of false positives:** Truncate the web-search list to the top 20 by relevance and ask the user to triage. Do not append unverified entries to the README.
- **README diff is huge (more than 500 lines changed):** Stop and ask the user whether to (a) apply in chunks per section, (b) accept the full rewrite, or (c) abort step 4. A wholesale README overwrite is a red flag.
- **Sub-agent exceeds its brief:** If a sub-agent edits files outside its authorized scope, the main agent reverts those changes (`git checkout -- <file>` for tracked files) and re-dispatches with a tighter brief.
- **`.oss-ready/` already has prior-run reports:** Don't overwrite. Append new runs as `<step>.<run-N>.md` and reference the prior run in the new report.
- **Target repo is the skills repo itself:** Stop. The skill is meant to operate on a *target* project, not on the skill catalog. Ask the user to `cd` into the target repo first.
- **`asm` / `gh` CLI missing:** Fall back to local-only checks for the audit and branch steps. Document the gap in the relevant `.oss-ready/<step>.md`.
- **Working tree dirty during a step:** Stash, run the step, pop. If pop conflicts, stop and ask the user.
