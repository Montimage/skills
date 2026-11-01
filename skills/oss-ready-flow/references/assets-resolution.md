# Resolving OSS Assets

Run this after the Dependency Preflight in SKILL.md, before copying any template. `OSS_READY_DIR` is the parent directory of the `skillMdPath` returned by `asm deps acquire oss-ready --session <caller-session-id> --json`. Use that path directly; never assume a relative sibling path such as `../oss-ready`. The lease belongs to the main agent's session: do not release it here, and do not call `asm cleanup` on this path.

```bash
set -e
if [ -z "$OSS_READY_DIR" ] || [ ! -d "$OSS_READY_DIR/assets" ] ||
   [ ! -f "$OSS_READY_DIR/assets/OSS_READINESS_CHECKLIST.md" ]; then
  echo "Incompatible or missing oss-ready at '$OSS_READY_DIR': assets/OSS_READINESS_CHECKLIST.md is required" >&2
  echo "Fix: asm install oss-ready, then re-run the Dependency Preflight" >&2
  exit 1
fi
# Preserve checklist progress on reruns; replacing it requires explicit approval.
checklist=docs/OSS_READINESS_CHECKLIST.md
if [ -d "$checklist" ]; then
  echo "Cannot copy checklist: $checklist is a directory" >&2
  exit 1
elif [ -e "$checklist" ] || [ -L "$checklist" ]; then
  echo "Existing $checklist preserved; replacement requires explicit approval" >&2
else
  # The approved destination may not exist in a fresh target repo.
  mkdir -p docs
  cp -n "$OSS_READY_DIR/assets/OSS_READINESS_CHECKLIST.md" "$checklist"
  if [ -d "$checklist" ] || [ -L "$checklist" ] || [ ! -f "$checklist" ]; then
    echo "Checklist copy failed: $checklist is not a regular file" >&2
    exit 1
  fi
fi
# Copy any other approved templates from "$OSS_READY_DIR/assets/" here.
```

Re-run the asset check before every copy, even if the preflight passed, because the installation may have changed since. If `OSS_READY_DIR` is empty or either asset check fails, stop; do not guess a relative path or continue with partial output. Use the same `$OSS_READY_DIR/assets/` prefix for every other approved template.
