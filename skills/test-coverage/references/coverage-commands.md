# Coverage Commands

Run the command matching the detected stack, preserving the project's existing configuration:

- Jest: `npx jest --coverage --coverageReporters=text --coverageReporters=json-summary`
- Vitest: `npx vitest run --coverage`
- Python: `python -m pytest --cov=. --cov-report=term-missing`
- Go: `go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out`
- Rust: `cargo tarpaulin --out Stdout`

Record the command, exit status, line/branch percentage, and uncovered paths. If the required tool or configuration is missing, report the exact prerequisite and stop before writing tests.
