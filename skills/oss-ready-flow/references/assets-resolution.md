# Resolving OSS Assets

Before copying a template, resolve the installed `oss-ready` skill directory and use its absolute path. The dependency preflight must run first. Preserve the exact borrowed path printed by `asm get`; do not canonicalize or replace it before cleanup:

```bash
set -e
BORROWED_PATH=''
cleanup_borrow() {
  if [ -n "$BORROWED_PATH" ]; then
    asm cleanup "$BORROWED_PATH"
  fi
}
trap cleanup_borrow EXIT
if ! BORROWED_PATH="$(asm get oss-ready --path 2>/dev/null)"; then
  echo "Unable to resolve installed skill: oss-ready; install/update it with asm" >&2
  exit 1
fi

if [ -z "$BORROWED_PATH" ] || [ ! -d "$BORROWED_PATH/assets" ] ||
   [ ! -f "$BORROWED_PATH/assets/OSS_READINESS_CHECKLIST.md" ]; then
  echo "Incompatible or missing oss-ready: assets/OSS_READINESS_CHECKLIST.md is required" >&2
  echo "Install/update oss-ready with asm before copying templates" >&2
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
  cp -n "$BORROWED_PATH/assets/OSS_READINESS_CHECKLIST.md" "$checklist"
  if [ -d "$checklist" ] || [ -L "$checklist" ] || [ ! -f "$checklist" ]; then
    echo "Checklist copy failed: $checklist is not a regular file" >&2
    exit 1
  fi
fi
# Copy any other approved templates from "$BORROWED_PATH/assets/" here.
```

The `EXIT` trap calls `asm cleanup` with the original non-empty stdout path after all copying and on every failure; an empty path is never cleaned up. Use the same borrowed prefix for other approved templates. Check the checklist file before `mkdir` or `cp`, even if preflight passed (the installation may have changed). If resolution or either asset check fails, stop; do not guess a relative path or continue with partial output.
