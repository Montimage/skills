# Phase 2 — Audit Report Template

Use this exact structure when reporting findings to the user. The headings, ordering, and severity labels are part of the contract — downstream tooling (and the Phase 3 plan) keys off them.

## Template

```markdown
# Supply Chain Audit — <repo name>

**Date:** <YYYY-MM-DD>
**Ecosystems detected:** npm, docker, github-actions
**Overall posture:** Moderate (see scoring.md)

## Executive summary

| Ecosystem        | Posture   | Critical | High | Medium | Low |
|------------------|-----------|---------:|-----:|-------:|----:|
| npm              | Weak      | 2        | 1    | 1      | 0   |
| docker           | Moderate  | 0        | 2    | 1      | 1   |
| github-actions   | Critical  | 3        | 1    | 0      | 0   |

Top three risks:

1. **No cooldown on npm installs** — recent npm attacks lived for hours; without `min-release-age`, malicious versions can reach this repo.
2. **GitHub Actions pinned by tag, not SHA** — a tj-actions–style compromise of any of the 7 listed Actions hits this workflow.
3. **Dockerfile base image uses `node:22`** — a moving tag; image content changes without code changes.

## Findings

### npm (in `./`)

#### npm-1 · Critical · Missing minimum release age

**Finding:** `.npmrc` does not set `min-release-age`. New transitive deps install immediately upon publication.

**Evidence:**
```
$ cat .npmrc
registry=https://registry.npmjs.org/
```

**Why it matters:** Most malicious npm versions are detected and yanked within 24–72h. A 2–7 day cooldown blocks the entire attack window.

**Recommended fix:** Add `min-release-age=7d` to `.npmrc` (full diff in Phase 3).

---

#### npm-2 · Critical · Postinstall scripts enabled by default

**Finding:** No `ignore-scripts` flag set. Installs run arbitrary code from every direct and transitive dependency.

**Evidence:** Default npm config; no `ignore-scripts=true` in `.npmrc` or `package.json`.

**Why it matters:** Postinstall is the #1 malware execution vector (eslint-config-prettier 2024, ua-parser-js 2021).

**Recommended fix:** Add `ignore-scripts=true` to `.npmrc`, plus a per-package allowlist for legitimate uses (Phase 3).

---

#### npm-3 · High · CI uses `npm install` instead of `npm ci`

**Finding:** `.github/workflows/ci.yml` line 14 uses `npm install`, which can mutate the lockfile mid-CI.

**Evidence:**
```yaml
- run: npm install && npm test
```

**Why it matters:** Non-deterministic installs defeat lockfile guarantees; an attacker who poisons a transitive dep can ship even with a lockfile present.

**Recommended fix:** Replace with `npm ci`. (Phase 3.)

<!-- continue per ecosystem -->

### docker

<!-- same structure -->

### github-actions

<!-- same structure -->

## Recommended changes (preview)

The fixes below are previewed only; full diffs and impact analysis are in the Phase 3 plan if you approve proceeding.

1. **npm-1, npm-2** → write `.npmrc` with `min-release-age=7d` and `ignore-scripts=true`. Impact: one-time pain when adding native modules.
2. **npm-3** → change CI install step to `npm ci`. Impact: none for healthy lockfiles.
3. **docker-1** → pin base image by digest. Impact: needs Renovate to keep current.
4. **gha-1** → pin all `uses:` lines to SHA. Impact: needs Renovate to bump; one-time mass edit.
5. **gha-2** → set `permissions: {}` at top level, grant per-job. Impact: any job that writes back needs explicit grants.

## Next step

Reply with one of:

- **"Plan it"** → I'll draft a change plan with full diffs (Phase 3).
- **"Plan a subset: <ids>"** → e.g., "Plan a subset: npm-1, npm-2, gha-1".
- **"Stop here"** → audit only; no plan.
```

## Rules when filling in the template

- **One finding per defect.** Don't combine "no lockfile and no cooldown" into one bullet — the user may want to fix one but not the other.
- **Quote evidence verbatim.** Paste the lines you read; don't summarize. The user needs to verify your interpretation.
- **"Why it matters"** must reference the attack class, not be generic. "Recent npm attacks live for hours" is good; "Best practice" is not.
- **Recommended fix** is a *pointer* to the Phase 3 plan, not the full plan itself. Keep it to one or two lines.
- **IDs** use `<ecosystem>-<number>` (e.g., `npm-1`, `docker-2`, `gha-3`). The same IDs are reused in Phase 3 so the user can approve a subset by ID.
- Severities follow the per-ecosystem references. Don't invent your own.
