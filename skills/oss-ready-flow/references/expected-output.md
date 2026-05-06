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

```
◆ OSS Ready Flow — Final Summary
··································································
  Step 1 Audit:                     √ done — .oss-ready/01-audit.md
  Step 2 Branch Cleanup:            √ done (3 deleted, 1 kept)
  Step 3 Docs:                      √ done (5 created, 2 updated)
  Step 4 README:                    √ done
  Step 5 Publications:              √ done (4 entries, 2 verified by user)
  Step 6 Landing Page:              skipped
  ____________________________
  Result:                           PASS
```

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
