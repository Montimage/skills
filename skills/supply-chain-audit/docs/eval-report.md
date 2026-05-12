<!--
AI-SKIP: This file is for human review only. Do not load it into agent
context as part of the skill's runtime instructions. If you are an AI
agent invoking `supply-chain-audit`, ignore this file entirely and read
`SKILL.md` in the parent directory instead.
-->

# Supply Chain Audit — Eval Report (iteration 1)

> **STOP — agents do not process this file.** This report is benchmarking artifact for humans evaluating the skill, not skill instructions. If you are an AI agent invoking `supply-chain-audit`, close this file and read `SKILL.md` in the parent directory. Loading this report into your context will not improve audit quality and will burn tokens.

**Skill version evaluated:** `supply-chain-audit` 1.0.0
**Date:** 2026-05-12
**Workspace:** `supply-chain-audit-workspace/iteration-1/` (sibling to the skill)
**Configurations compared:** `with_skill` (full SKILL.md + references loaded) vs `without_skill` (general-purpose agent, no skill)
**Runs per configuration:** 1

## Headline

| Configuration | Pass-rate (mean) | Total assertions | Avg time | Avg tokens |
|---|---:|---:|---:|---:|
| `with_skill` | **1.00** | 20/20 | 151.0 s | 50 909 |
| `without_skill` | 0.58 | 10/20 | 58.7 s | 28 926 |
| **Delta** | **+0.42** | **+10** | **+92.3 s** | **+21 983** |

The skill lifts pass-rate from 58 % to 100 % at a cost of ~2× tokens and ~2.5× wall time. The cost is concentrated in the two evals where the skill actively does work (1 and 2); on eval 3 the gap collapses because both configurations correctly do nothing.

## Eval-by-eval

### Eval 1 — `npm_audit_stops_at_phase_2`

Audits a Node project with no `.npmrc`, an empty lockfile, and a CI workflow that uses `npm install && npm test`. The skill must stop at Phase 2 and not edit anything.

| | with_skill | without_skill |
|---|---:|---:|
| Pass | **8/8** | 3/8 |
| Time | 209.8 s | 77.2 s |
| Tokens | 51 954 | 30 259 |
| Tool calls | 19 | 7 |

Baseline failed on: triggering as a defined skill, emitting a Phase 1 Detect block, emitting a Phase 2 executive-summary table, severity-tagging the cooldown and `ignore-scripts` findings as Critical, and stopping at the Phase 2 gate. The baseline produced reasonable findings but immediately offered "copy-paste patches" without phase gating — the four-phase contract is the skill's load-bearing feature here.

### Eval 2 — `subset_approval_applies_only_chosen_changes`

Audits a repo with `package.json`, an unpinned `Dockerfile` (`FROM node:22`), and a release workflow using `actions/checkout@v4`. The user pre-declares subset approval ("apply npm changes only"). The skill must produce a plan for all three ecosystems, then apply only the npm subset.

| | with_skill | without_skill |
|---|---:|---:|
| Pass | **8/8** | 3/8 |
| Time | 187.8 s | 62.7 s |
| Tokens | 67 942 | 29 784 |
| Tool calls | 38 | 13 |

Baseline failed on: detecting all three ecosystems (it missed the Docker and Actions findings entirely), gating Phase 3 after Phase 2, assigning stable IDs (`npm-1`, `docker-1`, `gha-1`), supplying diff/impact/reversibility blocks, and producing a Phase 4 completion report. The baseline also applied an unrelated change (it added `engines` and `license` fields to `package.json`) that the user never asked for — exactly the kind of scope creep the skill's "never include a change the audit didn't justify" rule blocks.

### Eval 3 — `no_ecosystem_detected_exits_cleanly`

Empty repo (just a `README.md`). Both configurations must refuse to fabricate findings.

| | with_skill | without_skill |
|---|---:|---:|
| Pass | **4/4** | 4/4 |
| Time | 55.4 s | 36.3 s |
| Tokens | 32 832 | 26 735 |
| Tool calls | 11 | 5 |

Non-discriminating: an unguided agent and the skill both correctly exit without inventing findings. Kept in the eval set as a negative control — a regression that makes the skill fabricate findings here would be a high-priority bug.

## Where the skill adds value

The differential is concentrated in three behaviors the assertion grader checks:

1. **Phase gating.** With-skill stops at Phase 2 and asks before planning; stops at Phase 3 and asks before applying. Baseline rushes from finding to patch.
2. **Evidence-based findings.** With-skill quotes fixture file contents verbatim per finding. Baseline mixes findings with generalized best-practice advice.
3. **Scope discipline on apply.** With-skill applies exactly the subset approved. Baseline applied changes the user did not ask for (`engines`, `license`).

## Where the skill costs you

- **Wall time** averages **+92 s** per audit. Most of that is reading the four reference files and producing the templated Phase 2 / Phase 3 markdown.
- **Tokens** roughly **double** the baseline. The reference files are the largest contributor (~16 KB total when all four are loaded).
- **Tool calls** are 2–3× higher because the skill reads each fixture file directly to quote it, rather than summarizing.

Whether this trade is worth it depends on the use case. For a one-shot pre-release audit: easily worth it. For a CI step running on every PR: probably not — use Renovate + a scanner instead.

## Methodology

1. **Fixtures** were generated as three local git repos with the exact contents named by each eval prompt. They are committed at HEAD so the grader can `git diff HEAD` to check for unauthorized edits.
2. **Subagents** ran each (eval × configuration) pair in parallel (one foreground, five backgrounded). Each `with_skill` subagent received the skill snapshot path, the fixture path, and the user prompt; each `without_skill` subagent received only the prompt and the fixture path.
3. **Outputs** were saved as `run.md` per-run plus any `applied/` artifacts the executor produced.
4. **Timing** (`total_tokens`, `duration_ms`, `tool_uses`) was captured from each subagent task notification at completion and written to `timing.json`. This is the only opportunity to capture it.
5. **Grading** is performed by `grade.py` — a per-assertion programmatic checker rather than the bundled LLM `grader.md`. Each assertion has its own predicate (regex over the transcript, git-status diff, file-content equality, etc.). Two regex bugs in the first run were corrected and the script re-run; final grades were spot-checked against the source `run.md` files.
6. **Aggregation** uses a small `aggregate.py` because the bundled `aggregate_benchmark.py` expects `eval-N/run-N/` directories and this run uses named eval directories with one run each. Schema matches `references/schemas.md` so the viewer can read it.

## Caveats

- **Single run per configuration.** No variance data. A 1.00 pass-rate on every with-skill assertion is suspicious in principle; in practice each assertion checks a structural feature the skill explicitly produces (a `◆ Audit` block, a `npm-1` ID, a `Reversibility:` line). Adversarial assertions worth adding next iteration:
  - "When asked to remove a `pull_request_target` workflow, the skill flags the workflow's intent before proposing deletion."
  - "When asked to skip the cooldown setting because of an emergency patch, the skill complies but warns in writing."
  - "When the user types `Approve all` for a plan containing a destructive change (e.g., deleting a workflow), the skill asks for re-confirmation."
- **Programmatic grader is brittle.** A future skill rewrite that renames `◆ Audit` to `■ Audit` or moves the completion block would silently fail assertions even though the skill behavior is fine. The fix is to keep the grader and the SKILL.md templates in sync — both live in this repo.
- **Eval 3 is non-discriminating** by design. Removing it would inflate the headline delta, but it's worth keeping as a regression guard.
- **No `pip` or pure-Python fixture** in this iteration. Coverage of the Python reference is therefore inferred from the npm pattern rather than directly tested.

## Reproducing

From the repo root:

```bash
WS=/Users/montimage/dev-montimage/skills/skills/supply-chain-audit-workspace/iteration-1

# Inspect the grading
ls "$WS"/*/with_skill/grading.json
cat "$WS/benchmark.md"

# Re-grade (idempotent; reads existing run.md files)
python3 "$WS/grade.py"

# Re-aggregate
python3 "$WS/aggregate.py"

# Re-open the interactive viewer
open "$WS/review.html"
```

To re-run the full eval (6 new subagent runs):

1. Delete `$WS` to start clean.
2. Re-run the skill's `evals/evals.json` against fresh fixtures via the parent agent.
3. Capture timing per task notification, then re-run `grade.py` + `aggregate.py`.

## Files

```
supply-chain-audit-workspace/iteration-1/
├── benchmark.json              # full benchmark data (viewer-compatible)
├── benchmark.md                # human-readable summary
├── review.html                 # static interactive viewer (133 KB)
├── grade.py                    # programmatic grader
├── aggregate.py                # per-run aggregator
├── skill-snapshot/             # frozen copy of supply-chain-audit at test time
├── fixtures/
│   ├── eval-1-npm/             # npm + Actions, no .npmrc
│   ├── eval-2-multi/           # npm + Docker + Actions
│   └── eval-3-empty/           # README.md only
├── npm_audit_stops_at_phase_2/
│   ├── eval_metadata.json
│   ├── with_skill/{outputs/run.md, timing.json, grading.json}
│   └── without_skill/{outputs/run.md, timing.json, grading.json}
├── subset_approval_applies_only_chosen_changes/  # same shape
└── no_ecosystem_detected_exits_cleanly/          # same shape
```
