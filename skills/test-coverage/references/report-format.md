# Report Format

Read this file at the end of each workflow step and before writing the final report in Step 4.

## Step Completion Report

After each of Steps 0-4, print this block. Use `√` for pass, `×` for fail, `—` for context.

```
◆ Step N — [step name]
··································································
  [check name]:   √ pass | × fail — [one-line reason]
  [measured value]: — [number, path, or command]
  Result:         PASS | FAIL | PARTIAL
```

Checks to list per step:

| Step | Checks |
| --- | --- |
| 0. Create Feature Branch | branch name; working tree clean after sync |
| 1. Analyze Coverage | detected stack and framework; coverage command and exit code; baseline line/branch percentages |
| 2. Identify Test Gaps | number of gaps selected; each gap has a source path:line |
| 3. Write Tests | test files created or updated; no duplicate test names or fixture conflicts |
| 4. Verify Improvement | same coverage command and exit code; before/after percentages; new tests pass |

If a check fails, mark `Result: FAIL` and stop. Ask the user how to continue.

## Final report

Default format: concise text with one before/after table. If the user requests another format, use it and keep the four items below. Do not produce an HTML or multimedia report for this skill.

Start the report with these four items, in this order:

1. **Result** — status first: `complete`, `partial`, or `blocked`. Then state what changed: test files added or updated, and the number of gaps covered.
2. **Evidence** — the coverage command, its exit code, and a table of before/after line and branch percentages per changed file and overall. Name the test command that passed.
3. **Uncertainty** — list gaps left uncovered with the reason (flaky, integration-only, generated, platform-specific, or out of scope). Label assumptions and inferences separately from measured numbers. A passing test proves only the behavior it asserts.
4. **Decision** — name the action that needs the user's approval (for example, merging the branch or changing coverage thresholds), or write `No approval needed.` List remaining user actions separately.

Example:

```text
Result: complete — added 9 tests in tests/test_parser.py covering 6 of 7 selected gaps.
Evidence: `pytest --cov=src --cov-branch` exit 0.
| Scope          | Lines before | Lines after | Branches before | Branches after |
| src/parser.py  | 71%          | 93%         | 58%             | 88%            |
| Overall        | 82%          | 86%         | 69%             | 75%            |
Uncertainty: src/parser.py:212 (network timeout branch) not covered — integration-only. Coverage numbers are measured; risk ranking of gaps is an inference.
Decision: No approval needed. Remaining user action: review and merge branch feat/test-coverage.
```

## Understanding checks

Grade the final report against these checks in addition to the Acceptance Criteria in SKILL.md:

- **Main result is findable** — the first line states the status and what changed, without reading logs.
- **Facts and assumptions are separated** — measured numbers name the command that produced them; assumptions, inferences, and untested paths are labeled.
- **Claims are traceable** — each coverage claim points to a command output or a source path:line; a passing test run does not imply that every gap is covered.
- **Next decision is clear** — the report names the required approval or states `No approval needed.`, and lists remaining user actions.

When a human reviewer is available, ask whether they could find the result, separate facts from assumptions, trace claims, and identify the next decision. If no reviewer answers, report human understanding as unconfirmed. Agent inspection does not confirm it.
