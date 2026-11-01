# Step Completion Reports

After each phase, print this compact status block. Use the check names listed for that phase. `√` is pass, `×` is fail, `—` adds context or marks a skipped check.

```
◆ Phase N — [phase name]
··································································
  [Check]:            √ pass | × fail — [reason]
  Result:             PASS | FAIL | PARTIAL
```

| Phase | Checks |
|---|---|
| 0 Resolve input | `Input format`, `URL validated` (or `—` local), `SKILL.md found` |
| 1 Research | `Scanner exit 0`, `Files analyzed N/N`, `Injection attempts` |
| 2 Report | `SKILL_AUDIT.md written`, `Secrets redacted`, `Findings cite path:line` |
| 3 Verdict | `Risk level`, `Verdict matches matrix` |
| 4 Install | `Install command built` (or `—` skipped), `User confirmed` |
