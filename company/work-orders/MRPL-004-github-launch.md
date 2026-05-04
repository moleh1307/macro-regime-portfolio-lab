# MRPL-004 - Initialize Local Git Baseline And Prepare GitHub Launch Boundary

- Owner role: Founder / Chief of Staff
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: local git repository

## Scope

- Initialize local git if needed.
- Commit the verified milestone 1 scaffold and report.
- Keep cached raw data out of git.
- Prepare the decision boundary for creating/pushing the public GitHub repo.

## Acceptance Criteria

- Local git repository exists.
- Initial commit captures source, config, tests, Specialist state, lockfile, and baseline report.
- Raw cached data and virtualenv/cache files are not staged.
- Public GitHub remote creation is not performed without explicit approval.

## Verification Evidence

- `git init` completed.
- Initial commit created: `af6cbe7 Initialize macro regime portfolio lab`.
- `git status --short` was clean after commit.
- `git remote -v` returned no configured remote.
- Raw cached data, `.venv`, pytest cache, ruff cache, and `__pycache__` are ignored.

## Blocker / Decision Needed

- Historical: public GitHub repo creation/push and license choice moved to MRPL-005.

## Closeout State

- Done.
