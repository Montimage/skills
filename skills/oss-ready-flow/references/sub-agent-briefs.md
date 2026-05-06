# Sub-agent Briefs (verbatim)

Use these as `prompt` arguments to the `Agent` tool, with `subagent_type: general-purpose`. Each brief is self-contained — the sub-agent has none of the main agent's context.

## Step 1 — Auditor (read-only)

> Run the `oss-ready` skill's Step 5 audit (8-section + bonus checklist) against the current repo. Do NOT create or modify files. Do NOT create a feature branch. Read-only audit only. For each checklist item return `{section, item, status: done|missing|n/a, evidence}`. Then write a markdown report to `.oss-ready/01-audit.md` with: (a) per-section pass/fail counts, (b) flat list of missing items, (c) flat list of items already done, (d) recommended priority order for the remaining steps. Return a 10-line summary to the main agent.

## Step 2 — Branch Analyst (read-only)

> Inventory all local and remote branches. For each branch, compute: ahead/behind counts vs. main, last commit date and author, whether it's merged into main (`git branch --merged main`), whether it has an open PR (`gh pr list --head <branch>`). Classify each branch into one of: `merged-safe-to-delete`, `unmerged-needs-review`, `stale-no-activity-90d`, `active-recent`, `protected-do-not-touch` (main, release/*, gh-pages). Write the report to `.oss-ready/02-branches.md` with a table per category and proposed action per branch. Do NOT delete or merge anything. Return a summary count per category.

## Step 3a — Docs Architect

> Read the codebase to identify the project type (CLI, library, web service, desktop app, etc.), tech stack, and existing docs. Decide which of the standard docs are needed: `docs/USER_GUIDE.md`, `docs/DEVELOPMENT.md`, `docs/DEPLOYMENT.md`, `docs/ARCHITECTURE.md`, `docs/API.md` (if applicable), `docs/CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`. For each missing doc, draft content based on actual code (entry points, configs, deploy scripts, CI workflows). For each existing doc, propose a diff. Write a plan to `.oss-ready/03-docs-plan.md` listing every file with action `create | update | keep` and a one-line rationale. Do NOT write the docs themselves yet. Return a summary table.

## Step 3b — Docs Writer

> Apply the approved plan from `.oss-ready/03-docs-plan.md`. For each file: write the new content (creates) or produce a diff and apply it (updates). Use the `oss-ready` skill's asset templates where applicable (`cp` LICENSE, CODE_OF_CONDUCT.md, SECURITY.md from oss-ready/assets — never read+write those files). For all other docs, base content on the actual codebase. After each file, run `git diff <file>` and capture the diff in `.oss-ready/03-docs-diffs.md`. Do NOT commit. Return a list of files written.

## Step 4 — README Polisher

> Read the current README and all files written in step 3. Produce a final README with these sections (drop any that don't apply): title + one-line tagline, badges (build, license, version, downloads if applicable), short description, key features, screenshots/demo (placeholder if assets aren't present — flag for user), quick start (< 5 min), installation, usage examples pulled from real code, configuration, project structure tree, links to docs/* files, contributing link, related publications placeholder (filled in step 5), license, acknowledgments. Cross-check every claim against the codebase: don't list a feature that isn't implemented; don't reference a config key that doesn't exist. Write the proposed README to `.oss-ready/04-readme-draft.md`. Produce a diff vs. current README in `.oss-ready/04-readme-diff.md`. Return a section-by-section change summary.

## Step 5 — Publications Researcher

> Scan the repo for any existing citation hints: `CITATION.cff`, `*.bib` files, README citation sections, papers in `docs/`, author names, project name variants. Compile a baseline list. Then ask the user (via the main agent) to provide additional known publications (DOIs, titles, conference names). If the user wants external search, use `WebSearch` / `WebFetch` to query Google Scholar, arXiv, Semantic Scholar with the project name and primary authors as cues. Compile a deduplicated list with for each entry: title, authors, year, venue, DOI/URL, one-line context (what they used the project for, if available). Write to `.oss-ready/05-publications.md` and propose a `## Related Publications` section for the README. Flag entries that need user verification.

The main agent must:

1. Pause the sub-agent after the baseline scan and ask the user for known publications.
2. Ask whether to do a web search.
3. Resume the sub-agent with the user's input.

## Step 6 — Landing Page Builder

> Scaffold a minimal GitHub Pages site at `docs/` (Jekyll) or `gh-pages-site/` (static) — pick based on what's already present. Create: `index.md` (or `index.html`) with project tagline, key features, quick start, links to docs and repo; `_config.yml` (Jekyll) with theme `minima` or `jekyll-theme-cayman`; `.github/workflows/pages.yml` if not present. Base all content on the README from step 4. Do NOT enable Pages remotely — produce instructions for the user to enable it via `gh repo edit` or repo settings. Write a plan to `.oss-ready/06-landing-page.md` and apply files only after main-agent confirmation. Return the list of files created.
