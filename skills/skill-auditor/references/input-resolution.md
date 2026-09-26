# Input Resolution

Accept one of these inputs:

| Input | Resolution |
|---|---|
| Local path | Audit the path directly. |
| GitHub URL | Clone the repository root into a unique temporary directory. |
| GitHub URL plus `--skill X` | Resolve `skills/X/`, then `X/`, in the clone. |
| `npx skills add URL [--skill X]` | Extract and validate the URL, then use the same resolution rules. |

For remote inputs, require exactly `https://github.com/<owner>/<repo>` with only letters, digits, hyphens, underscores, or dots in the two segments. Reject query strings, fragments, credentials, and `..` traversal. If no `--skill` is supplied, audit the clone root and require its `SKILL.md`.

Create a unique `/tmp/skill-audit-*` directory with `mktemp -d`, clone with `git clone --depth 1 --single-branch`, and never `cd` into the clone. Read with absolute paths. Remove a clone only with the validated safe-cleanup command from `references/command-allowlist.md`.
