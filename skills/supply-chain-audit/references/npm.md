# npm / pnpm / yarn — Audit and Remediation

Walk this checklist when the project has `package.json`. Each item is a binary check unless noted. The reference is structured so the parent SKILL.md can quote it directly in the audit report.

## Package manager detection

| Signal                     | Manager |
|----------------------------|---------|
| `package-lock.json`        | npm     |
| `pnpm-lock.yaml`           | pnpm    |
| `yarn.lock`                | yarn (v1 if `.yarnrc`, v2+ if `.yarnrc.yml`) |
| `bun.lockb`                | bun (treat as npm for this audit; flag bun specifics as `unknown`) |

If multiple lockfiles exist, that's a Critical finding by itself — the project has ambiguous reproducibility. List it as `multiple-lockfiles`.

## Audit checklist

### 1. Lockfile present and committed — **Critical**

- Check: lockfile exists, not in `.gitignore`, tracked by git (`git ls-files -- <lockfile>`).
- Bad: no lockfile, or lockfile ignored, or only `npm-shrinkwrap.json` with a stale `package-lock.json`.

### 2. Minimum release age (cooldown) — **Critical**

Read `.npmrc`, `.yarnrc.yml`, or `pnpm-workspace.yaml`.

- npm v11.10.0+: `min-release-age=` set to ≥ 2 days (ideal 7d).
- pnpm: `minimum-release-age` (kebab) or `minimumReleaseAge` (camel).
- yarn berry: `npmMinimalAgeGate: 60480` (seconds; 7d = 604800).
- yarn v1: no native support — flag as `unknown` and recommend Renovate config.

If absent or set to 0 / a few hours, finding is Critical. Most malicious npm versions are yanked within 24-72h.

### 3. Postinstall script execution — **High**

- Check `.npmrc` / `.yarnrc.yml` / `pnpm-workspace.yaml` for `ignore-scripts=true` (or pnpm's `enable-pre-post-scripts=false`).
- If unset, the default is to **run** scripts on install — that's the #1 malware execution vector. Flag High.
- Pre-1.0 packages that legitimately need postinstall (native modules, prisma, etc.) require a per-package allowlist. Note this in the impact when proposing the change.

### 4. CI uses deterministic install — **High**

Search workflows / `Makefile` / `package.json` scripts for the install command:

- npm: `npm ci` (good). `npm install`, `npm i` (bad — can mutate the lockfile).
- pnpm: `pnpm install --frozen-lockfile` (good). Plain `pnpm install` (bad in CI).
- yarn: `yarn install --frozen-lockfile` v1 or `yarn install --immutable` berry (good). Plain `yarn install` (bad).

If you can't find any CI config, mark as `unknown` (do not assume bad).

### 5. Audit command in CI — **Medium**

- Check workflows for `npm audit --audit-level=high`, `pnpm audit`, or `yarn npm audit`.
- Acceptable substitutes: `osv-scanner`, Snyk, Trivy, GitHub Dependabot alerts wired to fail CI.
- If none, finding is Medium.

### 6. Engines pinning — **Low**

- `package.json#engines.node` and `engines.npm` (or `engines.pnpm`) pinned to a range, not free-floating.
- If missing, Low. Useful but not critical.

### 7. Lockfile poisoning detection — **Medium**

- If a CI step like `lockfile-lint` or pnpm `--ignore-scripts --frozen-lockfile` audit isn't present, malicious lockfile edits can slip in via PR.
- Optional but recommended; flag Medium.

### 8. Provenance / attestations — **Low**

- For libraries publishing to npm: check `publishConfig.provenance` in `package.json` and whether release workflow uses `npm publish --provenance`.
- Skip if not a published package.

## Remediation snippets

The plan in Phase 3 uses these exact snippets. Adjust the `min-release-age` value if the user specified a different tolerance during Phase 2 review.

### `.npmrc` (npm)

```ini
# Block installs of packages published in the last 7 days.
# Most malicious versions are removed within 24-72h.
min-release-age=7d

# Disable lifecycle scripts on install (postinstall is the #1 malware vector).
# Re-enable per-package via `--foreground-scripts` for trusted packages.
ignore-scripts=true

# Fail noisy on audit issues during CI installs.
audit-level=high
```

### `.npmrc` (pnpm)

```ini
minimum-release-age=7d
ignore-scripts=true
audit-level=high
```

### `.yarnrc.yml` (yarn berry)

```yaml
npmMinimalAgeGate: 604800   # 7 days in seconds
enableScripts: false
```

### CI install step

```yaml
# .github/workflows/ci.yml — npm
- run: npm ci --audit=false
- run: npm audit --audit-level=high

# pnpm
- run: pnpm install --frozen-lockfile
- run: pnpm audit --prod --audit-level high

# yarn berry
- run: yarn install --immutable
- run: yarn npm audit --severity high
```

### Renovate cooldown preset (optional)

```json
// renovate.json
{
  "extends": ["config:recommended", "security:minimumReleaseAgeNpm"],
  "minimumReleaseAge": "3 days",
  "osvVulnerabilityAlerts": true
}
```

## Honest impact notes (use in Phase 3)

- **`ignore-scripts=true`** breaks packages that need postinstall: `node-sass`, `puppeteer`, `prisma`, native modules. Pair the change with a documented workaround (run `npm rebuild <pkg>` once, manually, after vetting).
- **`min-release-age=7d`** delays legitimate security patches by up to a week. Tell the user how to bypass for a specific install: `npm install <pkg> --no-min-release-age` (or via a temporary `.npmrc` override).
- **`npm ci` vs `npm install`** is purely a CI change — local dev keeps `npm install`. Don't propose changing every dev script; just CI.
- **Removing `yarn.lock` to migrate to pnpm** is *not* part of this skill's scope. Migration is a separate decision.
