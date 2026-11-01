# Expected Output

## Directory layout in the target repo after a successful run

```
target-repo/
├── .oss-ready/
│   ├── 01-audit.md            # Per-section audit results + priority list
│   ├── 02-branches.md         # Branch inventory + per-branch action log
│   ├── 03-docs-plan.md        # Doc create/update/keep plan
│   ├── 03-docs-diffs.md       # Diff for each updated doc
│   ├── 04-readme-draft.md     # Final README proposal
│   ├── 04-readme-diff.md      # Diff vs prior README
│   ├── 05-publications.md     # Repo-scanned + user-supplied + (optional) web entries
│   └── 06-landing-page.md     # Pages enable instructions (only if step 6 ran)
├── docs/
│   ├── USER_GUIDE.md
│   ├── DEVELOPMENT.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── README.md                  # Polished, with publications section
└── .github/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

## Final summary block emitted by the main agent

Open with the overall status, then fill all four parts. Keep it concise text; link to the `.oss-ready/` reports instead of inlining them.

```
◆ OSS Ready Flow — Final Summary
··································································
  Result:                           PASS — 5 of 6 steps done, Step 6 skipped by user
  Step 1 Audit:                     √ done — .oss-ready/01-audit.md (38/39 items)
  Step 2 Branch Cleanup:            √ done — .oss-ready/02-branches.md (3 deleted, 1 kept)
  Step 3 Docs:                      √ done — .oss-ready/03-docs-diffs.md (5 created, 2 updated)
  Step 4 README:                    √ done — .oss-ready/04-readme-diff.md (diff approved)
  Step 5 Publications:              √ done — .oss-ready/05-publications.md (4 entries)
  Step 6 Landing Page:              skipped (user declined)
  Files created/modified:           <list>
  Evidence:                         checks per step are in each report; git status shows N staged files
  Uncertainty:                      2 publications unverified by user; audit section 6 n/a (no gh auth)
  Decision:                         Approve or edit the suggested commit; no other approval needed
  Manual follow-ups:                gh repo edit --add-topic ...; enable GitHub Pages in repo settings
  Suggested commit:                 git commit -m "docs: prepare repository for open source release"
```

`Result` is `PASS` only when every step is `done` or user-`skipped` and the acceptance criteria in SKILL.md hold; otherwise `PARTIAL` (including a run the user stopped).

## Per-step Step Completion Report templates

### Step 1 — Audit

```
◆ Audit Current State (step 1 of 6 — <repo>)
··································································
  Section 1 License:                √ N/3
  Section 2 Codebase Cleanup:       √ N/5
  Section 3 Repository Setup:       √ N/5
  Section 4 Essential Docs:         √ N/5
  Section 5 Testing & Automation:   √ N/4
  Section 6 GitHub Settings:        √ N/5
  Section 7 Packaging:              √ N/3
  Section 8 Final Polish:           √ N/5
  Bonus items:                      √ N/4
  Report:                           .oss-ready/01-audit.md
  ____________________________
  Result:                           PASS | FAIL | PARTIAL
```

### Step 2 — Branch Cleanup Plan

```
◆ Branch Cleanup Plan (step 2 of 6 — <repo>)
··································································
  Total branches:                   N (local) + M (remote)
  Merged, safe to delete:           X
  Unmerged, needs review:           Y
  Stale (no activity 90d):          Z
  Active (recent):                  W
  Protected:                        V
  Report:                           .oss-ready/02-branches.md
  ____________________________
  Result:                           PARTIAL — needs user decisions
```

### Steps 3–6 — Docs, README, Publications, Landing Page

Emit this block after each of Steps 3, 4, 5, and 6 (use `skipped` when the user skipped the step):

```
◆ <Step name> (step N of 6 — <repo>)
··································································
  Files created:                    N
  Files updated:                    N
  Awaiting user approval:           N (list)
  Unverified items:                 N (list, e.g. publications to confirm)
  Report:                           .oss-ready/<NN-step>.md
  ____________________________
  Result:                           done | partial | skipped
```

## Review criteria for the Final Summary

Judge the Final Summary on understanding as well as correctness:

| Criterion | Observable check |
| --- | --- |
| Main result is findable | The first line states the overall status (`PASS` or `PARTIAL`) without opening any report. |
| Facts and assumptions are separated | Each `done` status names the report or check behind it; unverified items are listed under Uncertainty. |
| Claims are traceable | Every step line points to its `.oss-ready/` report; a written file is not reported as approved unless the user approved its diff. |
| Next decision is clear | The Decision line names the pending approval or says "No approval needed", and lists the user's manual follow-ups separately. |

When the run collects human feedback, ask the reviewer whether they could find the result, separate facts from assumptions, trace claims, and identify the next decision. If feedback is missing, blank, or nonresponsive, record human understanding as unconfirmed; agent inspection does not confirm it.
