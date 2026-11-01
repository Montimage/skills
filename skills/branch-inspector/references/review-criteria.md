# Review Criteria — Is the Output Understandable?

Correctness (the acceptance criteria in SKILL.md) is not enough. A run also passes when a human reviewer can use the output to decide. Check each criterion against the actual output:

| Criterion | Observable check |
|---|---|
| Main result is findable | The `Recommendation:` and `Reasoning:` lines and the step completion `Result:` line state the outcome without reading the full diff or logs. |
| Facts and assumptions are separated | Fields taken from git or `gh` output are stated as facts. Inferences (intent, conflict risk, recommendation) and skipped checks appear on the `Uncertainty:` line. |
| Claims are traceable | "What this branch implements" and each notable finding name a file, module, commit, or command result that supports it. A merge-status claim cites the `git cherry` count. |
| Next decision is clear | The overview ends with the four-option decision prompt. The action plan ends with an `Approval needed:` line naming the commands the user must run or approve, or `No approval needed` for keep. |

## Human feedback

When a human reviews the output, ask whether they could find the result, separate facts from assumptions, trace each claim, and identify the next decision. Record their answers with the run's feedback. If feedback is missing, blank, or unresponsive, report human understanding as unconfirmed. Agent inspection alone cannot confirm it.
