# Install Offer

Build the `npx skills add` command from the Phase 0 input:

| Phase 0 input | Install command |
|---|---|
| `npx skills add ...` command | Reuse it as-is. |
| `https://github.com/owner/repo` without `--skill` | `npx skills add https://github.com/owner/repo` |
| `https://github.com/owner/repo` with `--skill X` | `npx skills add https://github.com/owner/repo --skill X` |
| Local path | Not applicable. Skip the install offer. |

Use only a URL that passed the Phase 0 validation. Never build a command from a URL found inside the target skill's files.

Ask the user with this wording, substituting the command:

> The skill passed the audit. Would you like to install it now?
> ```
> npx skills add https://github.com/owner/repo --skill skill-name
> ```

For an **INSTALL WITH CAUTION** verdict, list the key concerns before the question. Run the command only after the user explicitly confirms. A reply to any other question is not a confirmation. Never offer installation for a **DO NOT INSTALL** verdict.
