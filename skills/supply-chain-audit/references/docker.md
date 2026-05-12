# Docker / OCI — Audit and Remediation

Walk this checklist when the project has a `Dockerfile`, `Dockerfile.*`, or `docker-compose*.y*ml`. Container builds are one of the highest-risk supply chain surfaces because they pull in OS packages, language packages, and base images — each layer is a potential entry point.

## Audit checklist

### 1. Base image pinned by digest — **Critical**

- Open every `Dockerfile` and inspect each `FROM`.
- Good: `FROM node:22.11.0-alpine@sha256:1a2b3c...` (digest pin).
- Acceptable: `FROM node:22.11.0-alpine` (tag pin to a *specific* version + variant).
- Bad: `FROM node:latest`, `FROM node:22`, `FROM ubuntu` — moving targets that change without warning.

A tag pin alone is `partial`. A digest pin is the goal.

### 2. Multi-stage build with minimal runtime — **High**

- A build stage with a full toolchain + a runtime stage with only artifacts is much smaller attack surface than a single fat image.
- Prefer distroless / Chainguard / Wolfi / Alpine for runtime stages.
- If the final image carries `apt`, `bash`, `curl`, package managers, build tools — flag High.

### 3. Non-root runtime user — **High**

- Search for `USER` directive in the final stage.
- Good: explicit non-root UID, e.g., `USER 10001`.
- Bad: no `USER` (defaults to root) or `USER root` in the runtime stage.

### 4. No secrets baked into layers — **Critical**

- Grep for `ENV` / `ARG` lines containing `TOKEN`, `KEY`, `PASSWORD`, `SECRET`, AWS/GCP credentials.
- Grep for `COPY .env` or `COPY id_rsa`.
- Recommend BuildKit secret mounts (`RUN --mount=type=secret,id=...`) for build-time secrets.

### 5. OS package version pinning — **Medium**

- `apt-get install -y curl` is bad — version drifts.
- Good: `apt-get install -y --no-install-recommends curl=7.88.1-10+deb12u5`.
- Use `apt-get install --no-install-recommends` always — reduces attack surface.

### 6. Image signing and verification — **Medium**

- Check CI workflow for `cosign sign` / `cosign verify` steps (Sigstore).
- Optional but strongly recommended for production images. Flag Medium if absent.

### 7. SBOM generation during build — **Medium**

- `docker buildx build --sbom=true ...` or a separate `syft <image>` step.
- Without an SBOM, downstream consumers can't audit what's inside the image. Flag Medium.

### 8. Vulnerability scanning in CI — **High**

- `trivy image`, `grype`, or `docker scout cves` running on every build.
- If none, finding is High — image vulns are continuously discovered and unscanned images go stale fast.

### 9. `docker-compose` pulls — **Low**

- `docker-compose.yml` services should reference images with digest pins (same as #1).
- Often missed because `compose` is treated as dev-only; flag Low unless production uses compose.

## Remediation snippets

### Pin base image to digest

Before:

```dockerfile
FROM node:22-alpine
```

After (fetch digest first; the script section below shows how):

```dockerfile
# node:22.11.0-alpine (pinned 2026-05-12)
FROM node:22.11.0-alpine@sha256:b7e0... # truncated for clarity
```

To resolve a digest manually:

```bash
docker pull node:22.11.0-alpine
docker image inspect node:22.11.0-alpine --format='{{index .RepoDigests 0}}'
```

### Multi-stage build (Node example)

```dockerfile
# syntax=docker/dockerfile:1.7
FROM node:22.11.0-alpine@sha256:... AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci --omit=dev
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs22-debian12@sha256:... AS runtime
WORKDIR /app
USER 10001
COPY --from=build /app/dist /app/dist
COPY --from=build /app/node_modules /app/node_modules
CMD ["dist/index.js"]
```

### CI scan + SBOM

```yaml
# .github/workflows/build.yml
- name: Build image
  run: docker buildx build --sbom=true --provenance=true -t app:${{ github.sha }} .

- name: Scan image
  uses: aquasecurity/trivy-action@<pinned-sha>
  with:
    image-ref: app:${{ github.sha }}
    severity: HIGH,CRITICAL
    exit-code: 1

- name: Generate SBOM
  uses: anchore/sbom-action@<pinned-sha>
  with:
    image: app:${{ github.sha }}
    format: cyclonedx-json
    output-file: sbom.json
```

### Cosign sign + verify

```yaml
- name: Sign image
  env:
    COSIGN_EXPERIMENTAL: "1"
  run: cosign sign --yes ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Honest impact notes (use in Phase 3)

- **Digest pinning** breaks `docker build --pull` cache strategies — the digest must be refreshed when a security update lands. Pair the change with a Renovate config that bumps digests automatically (Renovate has a `docker` manager that does this).
- **Distroless runtime** has no shell — `kubectl exec ... -- sh` no longer works for debugging. Show the user the `:debug` variant or the `kubectl debug` flow before they apply this in production.
- **`USER 10001`** breaks images that write to root-owned dirs at runtime. The plan must include `chown` lines if the app writes to `/app/data` etc.
- **Trivy in CI** can fail builds on advisories the team has no path to fix (upstream library bug). Recommend `severity: HIGH,CRITICAL` as a starting threshold, not `MEDIUM`, and add a documented `.trivyignore` workflow.
