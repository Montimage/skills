---
name: test-coverage
effort: high
description: Expand unit test coverage by targeting untested branches and edge cases. Use when users ask to "increase test coverage", "add more tests", "expand unit tests", "cover edge cases", "improve test coverage", "find untested code", "what's not tested", "run coverage report", "write missing tests", or want to identify and fill gaps in existing test suites. Adapts to project's testing framework. Trigger this skill whenever the user mentions test gaps, untested code, coverage percentages, or wants to harden their test suite.
metadata:
  version: 1.3.0
  creator: Montimage
---

# Test Coverage

Expand unit test coverage by targeting untested branches and edge cases.

## Repo Sync Before Edits (mandatory)

Before making any changes, sync with the remote to avoid conflicts:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is dirty, stash first, sync, then pop. If `origin` is missing or conflicts occur, stop and ask the user before continuing.

## Workflow

### 0. Create Feature Branch

Before making any changes:
1. Check the current branch - if already on a feature branch for this task, skip
2. Check the repo for branch naming conventions (e.g., `feat/`, `feature/`, etc.)
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/test-coverage`

### 1. Analyze Coverage

**Use sub-agents for parallel discovery.** Launch multiple Agent tool calls concurrently to keep the main context clean:

- **Agent 1 — Stack detection**: Scan for `package.json`, `tsconfig.json`, `pyproject.toml`, `setup.py`, `Cargo.toml`, `go.mod`, and identify the primary language(s), testing framework, and coverage tool. Check for existing test configuration (jest.config, vitest.config, pytest.ini, .coveragerc). Return a structured summary.
- **Agent 2 — Test inventory**: List all existing test files and directories, identify the testing patterns in use (file naming, directory structure, assertion style). Return a checklist of test locations and conventions.

Collect the results from both agents before proceeding.

Then run the appropriate coverage command for the project's stack:

```bash
# JavaScript/TypeScript (Jest)
npx jest --coverage --coverageReporters=text --coverageReporters=json-summary

# JavaScript/TypeScript (Vitest)
npx vitest run --coverage

# Python (pytest)
python -m pytest --cov=. --cov-report=term-missing

# Go
go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out

# Rust
cargo tarpaulin --out Stdout
```

From the report, identify:
- Untested branches and code paths (look for lines marked as uncovered)
- Low-coverage files/functions (below 80% line coverage)
- Missing error handling tests

### 2. Identify Test Gaps

**Use sub-agents for parallel file analysis.** When multiple low-coverage files are identified, dispatch independent agents to analyze them concurrently:

- **Agent per file group**: For each low-coverage file (or small group of related files), launch a sub-agent to read the source and identify specific untested code paths. Each agent should return a list of gaps with line numbers and suggested test scenarios.

Each agent should look for:
- **Logical branches**: if/else, switch/match, ternary operators
- **Error paths**: try/catch, error returns, validation failures
- **Boundary values**: min, max, zero, empty string, null/undefined, off-by-one
- **Edge cases**: empty collections, single-element collections, duplicate values
- **State transitions**: before/after mutations, async race conditions
- **Integration points**: API calls, database queries, file I/O

Collect all agent results and prioritize gaps by risk: error paths and boundary values cause the most production bugs.

### 3. Write Tests

Use the project's existing testing framework and follow its conventions. Detect which framework is in use by checking config files and existing test files.

| Stack | Framework | Test Location Pattern |
|-------|-----------|----------------------|
| JS/TS | Jest | `__tests__/` or `*.test.ts` |
| JS/TS | Vitest | `*.test.ts` or `*.spec.ts` |
| Python | pytest | `tests/` or `test_*.py` |
| Go | testing | `*_test.go` in same package |
| Rust | built-in | `#[cfg(test)]` module in same file |

**Use sub-agents for parallel test writing.** When gaps span multiple independent files or modules, dispatch sub-agents concurrently to write tests in parallel:

- **Agent per test file**: For each source file (or module) that needs new tests, launch a sub-agent to write the test cases. Each agent receives the gap analysis from Step 2 and the project conventions from Step 1. Each agent should return the path of the test file it created or updated.

Collect all agent results, then verify no conflicts between test files (e.g., duplicate test names, shared fixtures).

For each gap, write focused test cases:
- One assertion per logical concept (a test can have multiple asserts if they test the same behavior)
- Use descriptive names: `test_parse_returns_error_on_empty_input` not `test_parse_2`
- Group related tests logically (by function or behavior)

### 4. Verify Improvement

Run coverage again with the same command from Step 1 and confirm:
- New tests pass
- Coverage percentage increased
- Previously uncovered lines are now covered

Report the before/after coverage numbers to the user.

## Guidelines

- Follow existing test patterns and naming conventions in the project
- Add tests to existing test files when appropriate (don't create new files unnecessarily)
- Focus on meaningful coverage — skip trivial getters/setters unless they contain logic
- Use descriptive test names that explain the scenario being tested
- Avoid mocking unless the project already uses mocks extensively
