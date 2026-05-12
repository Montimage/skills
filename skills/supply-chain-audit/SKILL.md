---
name: supply-chain-audit
description: "Audit npm/pip/Docker/GitHub Actions for supply chain risks; apply cooldown, lockfile, ignore-scripts, SHA pinning, scanning after approval. Use for 'supply chain audit', 'harden dependencies'. Skip for runtime vulns, secret scanning, code review."
effort: high
metadata:
  version: 1.0.0
  author: Montimage
---

# Supply Chain Audit

Audits a project for the controls that block supply chain attacks — compromised packages, poisoned transitive dependencies, malicious post-install scripts, untrusted base images, hijacked GitHub Actions. Then proposes a layered remediation plan and applies it after explicit user approval.

The skill follows a strict four-phase workflow: **detect → audit → plan → apply**. Phase boundaries are gates the user crosses, not steps the agent powers through. Do not jump ahead.

## When to use

- The user says "audit supply chain", "harden dependencies", "avoid supply chain attack", "lock down npm/pypi".
- The user mentions a recent attack (Axios, TanStack, ultralytics, etc.) and wants to defend against the next one.
- The user is preparing a project for production / public release and wants the dependency surface tightened.

Do **not** use this skill for:

- Runtime application vulnerabilities (use a SAST/DAST tool or `code-review`).
- Secret scanning in commits (different attack vector).
- Generic dependency updates without a security goal (use Renovate/Dependabot directly).
- Cloud infra hardening (IAM, network policies) — out of scope.

## Repo Sync Before Edits (mandatory)

The apply phase mutates files in the repo (`.npmrc`, `pyproject.toml`, `Dockerfile`, workflow YAMLs). Before any edit, sync with the remote so changes don't land on a stale base:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty: `git stash` → sync → `git stash pop`. If `origin` is missing or a rebase conflict appears, stop and ask the user before continuing. Do not skip this — applying changes on a stale tree leaves the user with a confusing rebase to untangle.

## Inputs

The skill runs against the current working directory by default. If the user names a subdirectory ("audit `services/api`"), `cd` into it before detection. The skill never crosses repository boundaries on its own.

If the repo is a monorepo with multiple ecosystems (a `package.json` and a `pyproject.toml` and a `Dockerfile`), audit each in turn — do not silently pick one.

## Prerequisites

Verify before running. Stop and tell the user if any check fails.

- Current directory is inside a git repository (`git rev-parse --git-dir` succeeds). The skill needs git so it can show the user the exact diff before applying.
- At least one supported ecosystem manifest exists (see Phase 1). If none, tell the user and exit cleanly — there is nothing to harden.

## Phase 1 — Detect ecosystems

Identify which ecosystems are in play. The `scripts/detect_ecosystems.sh` helper prints one line per detected ecosystem; use it as a starting point and verify by reading the manifest files yourself.

Supported ecosystems:

| Ecosystem        | Trigger files                                                    |
|------------------|------------------------------------------------------------------|
| npm/Node         | `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` |
| Python           | `pyproject.toml`, `requirements*.txt`, `Pipfile`, `uv.lock`, `poetry.lock` |
| Docker           | `Dockerfile`, `Dockerfile.*`, `docker-compose*.y*ml`             |
| GitHub Actions   | `.github/workflows/*.y*ml`                                       |

If the repo has multiple, the audit covers each one and the report has one section per ecosystem. If none of these exist, exit with a one-line message ("No supported ecosystems detected — nothing to audit.") and stop.

For each ecosystem detected, read its reference file before auditing:

- `references/npm.md` — npm, pnpm, yarn checks and remediation.
- `references/python.md` — pip, uv, Poetry, Pipenv checks and remediation.
- `references/docker.md` — Dockerfile and image controls.
- `references/github-actions.md` — workflow pinning, permissions, OIDC.

Do **not** load reference files for ecosystems that aren't present. Token discipline matters here — a pure-npm project should never read `docker.md`.

Print the Phase 1 completion report:

```
◆ Detect (phase 1 of 4 — read-only)
··································································
  Git repository:        √ pass
  Manifest scan:         √ pass (N ecosystems found)
  Reference files read:  √ pass (npm, docker)
  Multiple-lockfile:     √ none | × flagged (note)
  Criteria:              √ 4/4 met
  ____________________________
  Result:                PASS
```

## Phase 2 — Audit and report

For each detected ecosystem, walk the **checklist** in its reference file. Each check resolves to one of:

- `present` — the control is in place and correctly configured.
- `partial` — the control exists but is weak (e.g., lockfile committed but no `npm ci` in CI).
- `missing` — the control is absent.
- `n/a` — does not apply (e.g., no CI yet).

Emit the audit report using the template in `references/audit-report.md`. The report must:

1. Begin with an **Executive summary** — one line per ecosystem with a posture rating (Strong / Moderate / Weak / Critical) computed per `references/scoring.md`.
2. List **Findings** grouped by ecosystem, sorted by severity (Critical → High → Medium → Low).
3. End with a **Recommended changes** preview — a numbered list of fixes the skill *can* apply, each with a one-line impact statement.

**Do not propose fixes for things you didn't actually inspect.** If you can't tell whether a control is in place (e.g., CI config in a private system), mark it `unknown` and ask the user.

After emitting the report, **stop and wait** for the user to decide whether to proceed to Phase 3. Do not auto-roll into planning. The audit alone is a valid deliverable.

Print the Phase 2 completion report:

```
◆ Audit (phase 2 of 4 — report only)
··································································
  Ecosystems detected:   √ pass (npm, docker, github-actions)
  Findings collected:    √ pass (N findings)
  Severities assigned:   √ pass
  Posture computed:      √ pass
  Criteria:              √ 4/4 met
  ____________________________
  Result:                PASS
```

## Phase 3 — Plan changes

Only enter Phase 3 if the user explicitly agrees. A reply like "looks good" or "interesting" is **not** approval to plan — ask "Shall I draft a change plan?" if intent is ambiguous.

Use the template in `references/change-plan.md`. For every proposed change, the plan must state:

- **File**: the exact path that will be created or modified.
- **Change**: the diff snippet (added / removed lines), not a prose summary.
- **Why**: one line linking back to a finding in the audit.
- **Impact**: what could break — developer ergonomics, CI duration, install behavior. Be honest about cost. Examples:
  - `ignore-scripts=true` breaks packages that legitimately need postinstall (e.g., native modules). Call this out.
  - A 7-day `min-release-age` delays security patches; tell the user how to fast-track an override.
  - Pinning Actions to SHA breaks `dependabot` auto-bumps unless paired with a SHA-aware updater.
- **Reversibility**: how to undo if the user regrets it (`git revert` is fine, but mention it).

Group changes by ecosystem, ordered by severity (apply Critical first). If two changes touch the same file, show them as one combined diff so the user can reason about the final state.

**Never include in the plan**: changes the audit didn't justify, "while I'm here" cleanups, refactors of unrelated code, dependency upgrades that aren't security-driven. Scope stays inside the audit's findings.

After emitting the plan, **stop and wait** for explicit approval. Ask: "Approve the plan, approve a subset (list IDs), or reject?" Accept partial approval — the user may want to skip the cooldown setting but accept everything else.

Print the Phase 3 completion report:

```
◆ Plan (phase 3 of 4 — proposed diffs, nothing applied)
··································································
  Findings covered:      √ N/N from audit
  Out-of-scope changes:  √ none
  Diffs included:        √ pass (every change has a diff block)
  Impact statements:     √ pass (every change names a downside)
  Reversibility lines:   √ pass
  Criteria:              √ 5/5 met
  ____________________________
  Result:                PASS
```

## Phase 4 — Apply

Only enter Phase 4 with explicit approval from Phase 3. If the user approved a subset, apply only those items.

For each approved change:

1. Read the target file (if it exists) before editing. Use `Read` then `Edit` — do not `Write` over a file blindly.
2. Apply the change exactly as it appeared in the plan. If you discover the file's actual contents differ from what the plan assumed, **stop**, tell the user, and ask whether to adjust.
3. After the edit, show a unified diff (`git diff -- <file>`) so the user sees what landed.

After all approved edits:

- Run the project's existing install/lint/test commands if cheap (`npm ci`, `uv sync`, `docker build --check`). Do not run anything that takes more than a minute without asking. If a check fails, surface the failure but do not auto-revert — let the user decide.
- Do **not** commit. Do **not** push. The user commits the diff themselves so they review it in their own tooling.
- Print the Phase 4 completion report:

```
◆ Apply (phase 4 of 4 — local changes only)
··································································
  Changes approved:      √ N items
  Changes applied:       √ N items
  Files modified:        √ <list>
  Sanity checks:         √ pass | × failed (note)
  Commit:                — left to user (intentional)
  Criteria:              √ 4/4 met
  ____________________________
  Result:                PASS
```

## Output and writing rules

- **Never invent findings.** If a check requires running a command you can't run in this environment, say so and skip the check — don't fabricate the answer.
- **Quote file contents verbatim** when reporting on them. Don't paraphrase `.npmrc` or a workflow YAML.
- **Severity discipline.** Reserve Critical for controls that actively prevent attacks documented in the wild (no cooldown, postinstall enabled, Actions pinned by tag). Reserve High for controls that materially reduce blast radius. Medium and Low are for hygiene.
- **Show the diff, not just the intent.** The user must be able to copy-paste your proposed change and see the same thing land.

## Optional follow-ups (offer only after Phase 4)

After applying, offer — don't auto-run:

- Set up Renovate or Dependabot with `minimumReleaseAge` (point to `references/renovate.md` if you add one later).
- Generate an SBOM with Syft (`syft . -o cyclonedx-json > sbom.json`).
- Schedule a follow-up audit in 90 days via `/schedule`.

## Reference index

- `references/npm.md` — npm/pnpm/yarn audit & remediation.
- `references/python.md` — pip/uv/Poetry/Pipenv audit & remediation.
- `references/docker.md` — Dockerfile and image checks.
- `references/github-actions.md` — workflow hardening.
- `references/audit-report.md` — Phase 2 report template.
- `references/change-plan.md` — Phase 3 plan template.
- `references/scoring.md` — posture rating rubric.
- `scripts/detect_ecosystems.sh` — one-liner ecosystem detection.
