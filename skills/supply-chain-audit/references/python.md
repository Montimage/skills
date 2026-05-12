# Python — Audit and Remediation

Walk this checklist when the project has any of: `pyproject.toml`, `requirements*.txt`, `Pipfile`, `setup.py`, `setup.cfg`. The reference is structured so the parent SKILL.md can quote it directly in the audit report.

## Package manager detection

Probe in this order; the first match is the project's primary manager.

| Signal                             | Manager      |
|------------------------------------|--------------|
| `uv.lock`                          | uv           |
| `poetry.lock` + `[tool.poetry]`    | Poetry       |
| `Pipfile.lock`                     | Pipenv       |
| `pdm.lock`                         | PDM          |
| `requirements*.txt` only           | pip          |
| `setup.py` / `setup.cfg` only      | legacy pip   |

If both `uv.lock` and `poetry.lock` exist, that's a Critical `multiple-lockfiles` finding — ambiguous reproducibility.

## Audit checklist

### 1. Lockfile present and committed — **Critical**

- Check the appropriate lockfile exists and is tracked by git.
- A bare `requirements.txt` without hashes is **not** a lockfile — flag this as `partial`.
- Recommendation: migrate to `uv` for free hashed lockfiles. Don't force the migration in Phase 3 unless the user agrees in Phase 2.

### 2. Hash pinning — **Critical**

- `uv.lock`, `poetry.lock`, `Pipfile.lock` already include hashes.
- For pip: `requirements.txt` must contain `--hash=sha256:...` lines; if any line is hashless, finding is Critical (one bad pin compromises the whole install).
- CI must use `pip install --require-hashes -r requirements.txt`. If not, flag as `partial`.

### 3. Minimum release age (cooldown) — **Critical**

- **uv** (`pyproject.toml`):
  ```toml
  [tool.uv]
  exclude-newer = "2026-05-05T00:00:00Z"
  ```
  Note: `exclude-newer` is a timestamp, not a duration. The cooldown is achieved by setting it to `now - 7d` and refreshing periodically. If missing, Critical.
- **Poetry, Pipenv, plain pip**: no native support. Cooldown must be enforced by Renovate / Dependabot. If neither is configured with `minimumReleaseAge`, flag Critical.

### 4. CI uses deterministic install — **High**

- uv: `uv sync --frozen` or `uv sync --locked` (good). Plain `uv sync` mutates the lockfile.
- Poetry: `poetry install --sync --no-root` is acceptable; `poetry lock --no-update` should run in CI to verify lockfile.
- Pipenv: `pipenv install --deploy --ignore-pipfile` (good). Plain `pipenv install` (bad).
- pip: `pip install --require-hashes -r requirements.txt` (good). Plain `pip install -r requirements.txt` (bad — drift).

### 5. Vulnerability scanning in CI — **High**

- `pip-audit` (PyPA, recommended) or `safety check` running in CI on every PR.
- Acceptable substitutes: `osv-scanner`, Snyk, GitHub Dependabot wired to fail CI.
- If none, finding is High.

### 6. setup.py / arbitrary code execution — **Medium**

Python packages can run arbitrary code during install via `setup.py` and PEP 517 build backends. There is no `ignore-scripts` equivalent.

- Check: does the project itself contain a non-trivial `setup.py`? If yes, recommend migrating to a declarative `pyproject.toml` (PEP 621) to reduce its own attack surface as a *publisher*.
- For *consumed* packages, the only defense is the cooldown (#3) plus scanning (#5). Note this clearly in the report.

### 7. Trusted publishing / provenance — **Low**

- If the project publishes to PyPI: check whether the release workflow uses PyPI Trusted Publishing (OIDC, no long-lived API token).
- Skip if not a published package.

### 8. SBOM generation — **Low**

- Optional: `syft .` or `cyclonedx-py` step in CI producing an SBOM artifact.
- Useful for downstream auditors; not blocking.

## Remediation snippets

### `pyproject.toml` (uv)

```toml
[tool.uv]
# Global cutoff: refuse to install package versions published after this
# RFC 3339 timestamp. Rotate to `now - 7d` weekly (CI cron, pre-commit, or
# Renovate). A fixed past timestamp freezes the entire dependency tree — that
# is NOT a cooldown, it is a freeze. The rotation is mandatory.
exclude-newer = "2026-05-05T00:00:00Z"

# Optional: per-package opt-out for trusted internal/build deps.
# exclude-newer-package = { setuptools = false }
```

Hash verification with uv is enforced at install time via the `--require-hashes`
CLI flag, not a `pyproject.toml` setting:

```bash
uv pip install --require-hashes -r requirements.txt
uv sync                                # uv.lock already carries hashes
uv build --require-hashes              # for publish workflows
```

### `pyproject.toml` (Poetry)

Poetry has no native cooldown. Pair with Renovate:

```toml
[tool.poetry.dependencies]
python = "^3.11"
# Pin direct deps to a compatible range; lockfile handles transitive.

[tool.poetry.group.dev.dependencies]
pip-audit = "^2.7"
```

```json
// renovate.json
{
  "extends": ["config:recommended"],
  "minimumReleaseAge": "7 days",
  "osvVulnerabilityAlerts": true
}
```

### `requirements.txt` migration to hashes (pip)

If the project uses bare `requirements.txt`:

```bash
# One-time: generate a hashed lockfile next to the .in file.
uv pip compile --generate-hashes requirements.in -o requirements.txt

# CI install:
pip install --require-hashes -r requirements.txt
```

If no `requirements.in` exists, propose creating one from the current `requirements.txt` (strip versions where pins are loose, then compile).

### CI scanning step

```yaml
# .github/workflows/ci.yml
- name: Install
  run: uv sync --frozen

- name: Scan deps
  run: |
    uv pip install pip-audit
    pip-audit --strict --requirement requirements.txt
```

### Renovate cooldown preset (cross-manager)

```json
{
  "extends": ["config:recommended"],
  "minimumReleaseAge": "7 days",
  "osvVulnerabilityAlerts": true,
  "packageRules": [
    {
      "matchManagers": ["pip_requirements", "poetry", "pep621"],
      "minimumReleaseAge": "7 days"
    }
  ]
}
```

## Honest impact notes (use in Phase 3)

- **`exclude-newer` (uv)** must be **rotated** (cron, pre-commit, or Renovate-managed). A pin to a fixed date six months ago means new packages are blocked entirely — that's not a cooldown, it's a freeze. The plan must include the rotation mechanism.
- **`--require-hashes`** breaks any install that adds a dep without regenerating the lockfile. Tell the user that `pip install <pkg>` no longer works ad-hoc; they must update the `.in` file and recompile.
- **Migrating to uv** is the biggest unlock here (hashes + cooldown out of the box) but is a bigger change than the user may have asked for. Offer it in Phase 2 as a Strong recommendation; do not silently migrate in Phase 4.
- **`pip-audit --strict`** can fail builds on unrelated upstream advisories. Tell the user there's a 1-2 week tolerance window after a new CVE drops before they can patch.
