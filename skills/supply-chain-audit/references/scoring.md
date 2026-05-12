# Posture Scoring Rubric

How to translate per-ecosystem findings into the Strong / Moderate / Weak / Critical posture rating shown in the Phase 2 executive summary.

The rubric is intentionally coarse — four bins, not a 100-point score. Users react to "Weak" or "Critical" faster than to "68/100".

## Algorithm

For each detected ecosystem, count findings by severity:

| Findings observed                                          | Posture    |
|------------------------------------------------------------|------------|
| 0 Critical, 0 High, ≤ 2 Medium, any Low                    | **Strong** |
| 0 Critical, 1–2 High, any Medium, any Low                  | **Moderate** |
| 0 Critical, 3+ High **OR** 1 Critical                      | **Weak**   |
| 2+ Critical                                                | **Critical** |

Special cases:

- **`multiple-lockfiles`** or **`pull_request_target` with checkout of head** alone forces the ecosystem to **Critical** even if everything else is clean. These are RCE-class exposures.
- An ecosystem with zero applicable controls (e.g., a `Dockerfile` that's never built in CI) can drop one severity tier on appeal — note this in the report.

## Overall repo posture

The repo's overall posture is the **worst** ecosystem posture, not an average. A Strong npm setup paired with a Critical Actions setup is still a Critical repo — the weakest link sets the rating.

## When to refuse to score

Refuse to assign a posture (and say so) if:

- More than half the checks for an ecosystem returned `unknown` (you couldn't inspect them).
- The repo lacks CI but is published / deployed externally — the audit only saw half the surface.

In both cases, label posture as **Indeterminate** and explain what would have to be checked to upgrade the rating.

## Why this rubric

The thresholds are calibrated against the cooldown-and-pinning checklist that would have blocked the 2024–2026 wave of public incidents:

- **Strong** = would have blocked Axios 2025, TanStack 2025, eslint-config-prettier 2024, tj-actions/changed-files 2024, ultralytics 2024.
- **Moderate** = would have blocked the package-manager incidents, but not the Actions one.
- **Weak** = vulnerable to one or two of the listed incidents.
- **Critical** = vulnerable to most.

If the user pushes back ("we have Snyk, why are we Weak?"), explain the gap — Snyk catches *known* CVEs after disclosure; the cooldown gates the window where a 0-day malicious version exists in the registry before disclosure. They're complementary, not substitutes.
