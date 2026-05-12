# GitHub Actions — Audit and Remediation

Walk this checklist for every file under `.github/workflows/`. CI/CD is now a top supply-chain attack vector (tj-actions/changed-files compromise, reviewdog token exfiltration, GitHub Actions cache poisoning) — the defenses below blunt all three.

## Audit checklist

Iterate over each workflow file. Report per-file findings, then aggregate at the workflow-suite level.

### 1. Actions pinned by commit SHA — **Critical**

For every `uses:` line:

- Good: `uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1` (full 40-char SHA + comment).
- Bad: `uses: actions/checkout@v4` (mutable tag), `uses: actions/checkout@main` (extremely dangerous).
- Exception: `uses: ./.github/actions/local-thing` (local actions — same risk as the rest of the repo).

A single `@v4` somewhere is enough for an attacker who hijacks `actions/checkout@v4` to compromise the entire workflow. Flag Critical even if just one Action is loosely pinned.

### 2. `permissions:` set to least privilege — **High**

- Top-level `permissions: read-all` or `permissions: {}` is good.
- Per-job permissions narrower than top-level is even better (`contents: read`, then `id-token: write` only where needed).
- No `permissions:` block means the default token has `contents: write` everywhere — flag High.

### 3. OIDC for cloud / registry auth — **High**

- Check for `id-token: write` paired with `aws-actions/configure-aws-credentials` / `google-github-actions/auth` / `azure/login` using OIDC.
- Bad: long-lived `${{ secrets.AWS_ACCESS_KEY_ID }}` / `secrets.NPM_TOKEN` / `secrets.PYPI_TOKEN`.
- Recommended: PyPI Trusted Publishing, npm provenance with OIDC, AWS/GCP OIDC roles.

### 4. `pull_request_target` usage — **Critical (if found)**

- Search workflows for `pull_request_target`. This event runs in the **base repo context** with secrets — checking out the PR head and running code is a remote-code-execution primitive.
- If found, inspect carefully. Acceptable: a workflow that only labels / comments without checking out PR code. Bad: any `checkout` of PR head + script execution.

### 5. Workflow concurrency and timeouts — **Low**

- `timeout-minutes:` on every job (default is 360 — too long, lets an attacker exfiltrate longer).
- `concurrency:` group to prevent duplicate runs being used for race conditions.

### 6. Cache poisoning protection — **Medium**

- `actions/cache` keyed on lockfile hash, scoped per-branch — that's the default for the `setup-*` actions, fine.
- A custom cache step that includes user-controlled input in the key is dangerous; flag if seen.

### 7. Secrets scoped to environments — **Medium**

- Production secrets (publish tokens, signing keys) belong in GitHub Environments with required reviewers, not repo-level secrets.
- Check `environment:` declarations on jobs that use those secrets.

### 8. `script` injection in `run:` steps — **High**

- Any `run:` step that interpolates `${{ github.event.* }}` directly into a shell command is a script-injection bug.
- Bad: `run: echo "PR title: ${{ github.event.pull_request.title }}"` — an attacker controls the title.
- Good: pass via env var: `env: { TITLE: "${{ github.event.pull_request.title }}" }` then `run: echo "PR title: $TITLE"`.

### 9. Third-party Action provenance — **Medium**

- For non-`actions/*` and non-vendor Actions, prefer ones with signed releases (verifiable via Sigstore) and active maintenance.
- Flag Medium if the workflow uses an Action with < 100 stars and no recent activity (judgment call, document the reasoning).

## Remediation snippets

### Pin Actions by SHA

For each `uses: org/action@vX` line, resolve the SHA:

```bash
# Manual:
gh api repos/actions/checkout/git/ref/tags/v4.1.1 --jq .object.sha

# Or use a maintained tool:
npx pin-github-action .github/workflows/ci.yml
```

After pinning:

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
- uses: actions/setup-node@1e60f620b9541d16bece96c5465dc8ee9832be0b # v4.0.3
```

Pair with Renovate so SHAs are auto-bumped:

```json
{
  "extends": ["config:recommended", "helpers:pinGitHubActionDigests"]
}
```

### Least-privilege permissions

```yaml
# Top-level default — denies everything not explicitly granted per-job.
permissions: {}

jobs:
  build:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps: [...]

  publish:
    permissions:
      contents: read
      id-token: write   # for OIDC; required for trusted publishing.
    needs: build
    runs-on: ubuntu-latest
    steps: [...]
```

### OIDC publish (PyPI example)

```yaml
- uses: pypa/gh-action-pypi-publish@<pinned-sha>
  with:
    # No password / api token — OIDC handshake supplies a short-lived token.
```

Configure PyPI Trusted Publishing pointing at the repo + workflow + environment.

### Safe interpolation of event payload

```yaml
- name: Comment on PR
  env:
    TITLE: ${{ github.event.pull_request.title }}
    BODY: ${{ github.event.pull_request.body }}
  run: |
    echo "Title: $TITLE"
    echo "Body: $BODY"
```

### Workflow scanner (recommended in CI)

```yaml
- name: Lint workflows
  uses: returntocorp/semgrep-action@<pinned-sha>
  with:
    config: p/github-actions
```

Or use [`zizmor`](https://github.com/woodruffw/zizmor):

```yaml
- uses: actions/checkout@<pinned-sha>
- name: zizmor
  run: |
    pip install zizmor
    zizmor .github/workflows/
```

## Honest impact notes (use in Phase 3)

- **SHA pinning** kills the "auto-update to latest minor" benefit of `@v4`. Pair every SHA pin with a Renovate rule, or the user is signing up for stale Actions forever.
- **`permissions: {}`** breaks anything that writes back to the repo (release jobs, doc bots, commit-back patterns). Each affected job needs explicit grants — the plan must list those grants, not just the top-level lockdown.
- **OIDC migration** requires configuration on the cloud / registry side (AWS IAM role trust policy, PyPI Trusted Publisher entry). Don't pretend the workflow change is the whole story; the user has work to do off-GitHub.
- **`pull_request_target` removal** may break workflows that intentionally use it for labeling forked PRs. Don't blindly delete — propose `pull_request` + careful guarding instead, and flag the trade-off.
