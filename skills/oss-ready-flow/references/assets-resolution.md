# Resolving OSS Assets

Before copying a template, resolve the installed `oss-ready` skill directory and use its absolute path. The dependency preflight must run first. Preserve the exact borrowed path printed by `asm get`; do not canonicalize or replace it before cleanup:

```bash
set -e
BORROWED_PATH="$(asm get oss-ready --path 2>/dev/null || true)"
cleanup_borrow() {
  if [ -n "$BORROWED_PATH" ]; then
    asm cleanup "$BORROWED_PATH"
  fi
}
trap cleanup_borrow EXIT

if [ -z "$BORROWED_PATH" ] || [ ! -d "$BORROWED_PATH/assets" ]; then
  echo "Missing required skill or assets: oss-ready/assets" >&2
  echo "Install it:      asm install oss-ready -p claude --yes" >&2
  echo "No asm yet:      npm install -g agent-skill-manager" >&2
  echo "Verify:          asm list -p claude --json | grep 'oss-ready'" >&2
  exit 1
fi
cp "$BORROWED_PATH/assets/OSS_READINESS_CHECKLIST.md" docs/OSS_READINESS_CHECKLIST.md
# Copy any other approved templates from "$BORROWED_PATH/assets/" here.
```

The `EXIT` trap calls `asm cleanup` with the original non-empty stdout path after all copying and on every failure; an empty path is never cleaned up. Use the same borrowed prefix for other approved templates. If resolution or the `assets/` check fails, stop; do not guess a relative path or continue with partial output.
