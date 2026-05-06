# Example Output

A worked example of a complete Branch Overview block:

```
◆ Branch Overview: feature/old-payment-flow
··································································
  Refs:               local=yes remote=yes in-sync=yes
  Tip:                a1b2c3d 2025-09-14 by alice
  Diverged at:        7f8e9d0 2025-07-02
  Activity:           23 commits ahead, 184 commits behind main
                      last commit 234 days ago
  Authors:            alice, bob
  Diff:               41 files, +2310/-870 lines
  Top areas:          src/payments, src/api, tests/payments
  Merge status:       unmerged (cherry-equivalent: 0/23)
  Linked PR:          none
  Conflict risk:      high — 12 files overlap recent main activity
  Staleness:          abandoned (>90d)
  Intent:             feature (payment provider swap)

What this branch implements:
Replaces the Stripe-only payment integration with a provider-abstraction
layer supporting Stripe and Adyen. Adds src/payments/provider.ts as the
new interface, refactors src/api/checkout.ts to call it, ports existing
tests, and adds 6 new tests for Adyen. Three commits at the tip are
"WIP" with no tests; the Adyen webhook handler is unfinished.

Notable findings:
- 184 commits behind main; checkout.ts has been rewritten upstream — high conflict risk
- Last 3 commits are WIP, webhook handler returns a TODO
- No CI run on tip

Recommendation: archive
Reasoning: substantial work worth preserving but stale and conflict-heavy; not viable as a PR without a major rebase.
```

The decision prompt that follows:

```
What would you like to do with this branch?

  1. Delete   — already-merged or abandoned, nothing worth saving
  2. Archive  — preserve the work, remove from active branch list
  3. Open PR  — branch is ready or close to ready for review
  4. Keep     — still in active development, no action now

(For archive: tag-and-delete, or rename to archive/<branch>?)
```

The action plan that follows the decision matches the chosen template in `action-plans.md`, with `<branch>` substituted and (for PR) the suggested title/body filled in from the implementation summary above.
