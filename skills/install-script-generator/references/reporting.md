# Reporting — step reports, final response, review criteria

Read this file before Phase 1 and again before Phase 5.

## Step Completion Reports

Print this block after each phase (1-5). Use `√` for pass, `×` for fail, `—` for context.

```
◆ Phase N — [phase name]
··································································
  Output file:      env_info.json          √ written
  Check:            [the phase's done-condition]  √ pass | × fail
  Blockers:         none | [what stopped the phase]
  Result:           PASS | FAIL | PARTIAL
```

Done-conditions per phase:

| Phase | Done when |
| --- | --- |
| 1 Environment | `env_info.json` exists and `summary.primary_package_manager` is not null, or the user answered the no-package-manager question |
| 2 Planning | `installation_plan.yaml` exists and every step has `command` and `verify` |
| 3 Execution | the `--dry-run` pass printed every step, then the real run exited 0; a non-zero exit is FAIL |
| 4 Documentation | `install_report.md` and `USAGE_GUIDE.md` exist and name the target and platform |
| 5 Final response | the response below is printed |

## Final response contract

Default format: concise text, under 15 lines, followed by the output file table. Use a longer format only when the user asks for one. If a file could not be written, print its content inline and say so.

The response states these four items, in this order:

1. **Result** — `COMPLETE`, `PARTIAL` (a non-critical step failed or was skipped), or `BLOCKED` (a critical step failed), plus the target and platform.
2. **Evidence** — the checks actually run: each `verify` command and its exit status, the executor exit code, and the paths of the files written. Quote the failing step name and its stderr line on failure.
3. **Uncertainty** — label separately from verified facts: steps without a `verify` command, non-critical steps that failed, rollbacks that ran without their own verification, and platform behavior assumed rather than observed. A dry run proves only that the plan parses, not that installation works.
4. **Decision** — the action the user must take next (for example, rerun with sudo, pick a package manager, or approve a manual step), or `No approval needed.`

## Review criteria for understanding

Use these alongside the correctness criteria in SKILL.md → Acceptance Criteria when grading an output.

- **Main result is findable** — the first line of the final response states the status and target without reading logs.
- **Facts and assumptions are separated** — verified claims name the command that was run; assumed or untested behavior is labeled.
- **Claims are traceable** — every success claim points to a `verify` result or file path; a passed dry run is never reported as an installed package.
- **Next decision is clear** — the response names the required user action or states `No approval needed.`

If no human reviewer gives feedback, or the feedback is blank, record human understanding as unconfirmed. Agent inspection cannot confirm it.
