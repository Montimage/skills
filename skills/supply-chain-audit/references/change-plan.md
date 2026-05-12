# Phase 3 — Change Plan Template

Use this exact structure when proposing changes. Each change is keyed to a finding ID from the Phase 2 report so the user can approve a subset by ID.

## Template

```markdown
# Supply Chain — Change Plan

**Based on:** audit report dated <YYYY-MM-DD>
**Total changes:** N (Critical: a, High: b, Medium: c, Low: d)

---

## npm-1 + npm-2 — Cooldown and script gate

**Files touched:**
- `.npmrc` (create or modify)

**Diff:**
```diff
# .npmrc
+# Block installs of packages published in the last 7 days.
+# Most malicious npm versions are detected and yanked within 24-72h.
+min-release-age=7d
+
+# Disable lifecycle scripts on install.
+# Re-enable per trusted package via documented allowlist below.
+ignore-scripts=true
+
+audit-level=high
```

**Why:** Addresses npm-1 (Critical) and npm-2 (Critical) from the audit. Blocks the two highest-leverage npm attack patterns at once.

**Impact (read before approving):**

- **Breaks packages with legitimate postinstall.** Known cases in this repo: `prisma` (would need `npx prisma generate` manually). Run `grep -l '"postinstall"' node_modules/*/package.json` after install to see who is silently relying on it.
- **Slows in security patches.** A 7-day cooldown means an emergency upstream patch won't reach this repo for a week. Override for a one-off install: `npm install <pkg> --no-fund --foreground-scripts --omit=optional` plus a temporary `.npmrc` with `min-release-age=0d`.
- **Local dev unchanged** unless devs install new packages — the cooldown only fires on *new* package versions.

**Reversibility:** `git revert <commit>` reverts the `.npmrc`. Cached `node_modules` are unaffected.

---

## npm-3 — CI uses `npm ci`

**Files touched:**
- `.github/workflows/ci.yml`

**Diff:**
```diff
   - name: Install
-    run: npm install
+    run: npm ci
```

**Why:** Addresses npm-3 (High). `npm ci` refuses to mutate the lockfile mid-CI; `npm install` can silently rewrite it.

**Impact:** Builds will now fail if `package.json` and `package-lock.json` are out of sync — that's the desired behavior. Devs who edit `package.json` must run `npm install` locally and commit the resulting lockfile.

**Reversibility:** Trivial — single line.

---

## docker-1 — Pin base image by digest

**Files touched:**
- `Dockerfile`

**Diff:**
```diff
-FROM node:22-alpine
+# node:22.11.0-alpine pinned 2026-05-12
+FROM node:22.11.0-alpine@sha256:b7e08bf6ac17c2c84e2f60af0fcb01ed3a2dd2db... AS build
```

**Why:** Addresses docker-1 (Critical). A digest pin makes the base image immutable; a tag like `node:22` silently swaps when Docker Hub rebuilds.

**Impact:**

- **Breaks `docker build --pull` strategy.** The digest is now the source of truth, not the tag.
- **Requires Renovate or manual rotation.** Without an updater, the digest goes stale and you'll miss base-image CVE patches. Adding `renovate.json` is part of this change (see docker-1b).
- **CI cache invalidation.** The next build will re-pull the base layer (one-time cost).

**Reversibility:** Replace digest with previous tag if Renovate hasn't run yet; otherwise `git revert`.

---

<!-- One block per change. Group multi-file changes touching the same file. -->

## Approval

Reply with one of:

- **"Approve all"** → I apply every change above.
- **"Approve: npm-1, npm-2, gha-1"** → subset by ID.
- **"Approve all except docker-1"** → exclude by ID.
- **"Reject"** → no changes; stop.

Partial approval is fine. I will apply only what you approve and re-emit Phase 4 with the actual diffs that landed.
```

## Rules when filling in the template

- **Diffs, not prose.** "Add `min-release-age=7d`" is wrong. The actual unified diff is right. The user must be able to mentally apply your diff and predict the file state.
- **Honest impact statements.** Every change has a downside; if you can't name one, you don't understand the change well enough to apply it. Use the per-ecosystem "Honest impact notes" sections as a starting point.
- **Group related changes** under one section if they share a file or rationale. Don't split `min-release-age` and `ignore-scripts` into two sections — they live in the same file and serve the same goal.
- **Show the surrounding context** in diffs (one or two unchanged lines above/below) so the user can place the change.
- **Never include a change that wasn't a finding.** "While we're here, let me add Husky pre-commit hooks" is not in scope.
- **Reversibility line** is required on every change. Even if it's "trivial — single line revert", say so.

## Approval semantics

- "Approve all" = apply every block.
- "Approve: <ids>" = whitelist; everything else is skipped.
- "Approve all except <ids>" = blacklist.
- Ambiguous ("looks good") = ask "Approve all, or a subset?" Do not assume.
- After applying, Phase 4 reports the actual diffs that landed and any sanity-check failures.
