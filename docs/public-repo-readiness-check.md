# Public Repo Readiness Check

## Purpose

MRPL-027 checks whether the current repository state is ready to present as a
public GitHub portfolio artifact for milestone 2.

This is not a methodology review and does not change quantitative outputs.

## Result

Milestone 2 is presentation-ready as a reproducible research-process artifact.

No release tag was created. A tag or formal release should still require an
explicit release-boundary decision.

## Checks Performed

| Check | Result |
| --- | --- |
| README scanability | Pass |
| Docs navigation | Pass |
| Local Markdown links | Pass |
| Claim-boundary scan | Pass |
| Unit tests | Pass: 38 tests |
| Ruff lint | Pass |
| Git working tree before closeout | Clean before this report |
| Remote `main` before closeout | `b6c10ed` |

## Navigation Review

The README now gives a GitHub reader:

- a clear project description;
- a compact status table;
- quick-start commands;
- a "How To Read Results" section;
- a direct link to the milestone 2 summary;
- a direct link to the docs index.

`docs/index.md` provides a readable methodology trail:

- start-here documents;
- methodology path;
- validation and monitoring path;
- explicit reading boundary.

No broken local Markdown links were found in `README.md` or `docs/*.md`.

## Claim-Boundary Review

Public-facing language remains conservative.

Allowed framing currently present:

- reproducible public-data research pipeline;
- regime-aware ETF allocation research;
- diagnostic evidence;
- partial locked validation;
- turnover-stability repair;
- fresh-data-forward monitoring scaffold;
- no completed forward-monitoring returns yet.

Forbidden framing was not used as a positive claim:

- robust outperformance;
- validated strategy;
- investment-ready allocation;
- live trading system;
- alpha model;
- production optimizer;
- fresh validation after the post-holdout-review cycle.

The forbidden phrases still appear in docs only as explicit "not allowed" or
claim-boundary language, which is appropriate.

## Reproducibility Review

The README quick-start commands cover the current scripted workflow:

```bash
uv sync
uv run pytest
uv run python scripts/fetch_data.py
uv run python scripts/run_baseline_backtest.py
uv run python scripts/build_features.py
uv run python scripts/run_walk_forward.py
uv run python scripts/run_robustness_review.py
uv run python scripts/run_validation_protocol.py
uv run python scripts/run_turnover_stability_protocol.py
uv run python scripts/run_fresh_forward_monitoring.py
```

The current readiness check ran:

```bash
uv run pytest
uv run ruff check .
```

Both passed.

## Remaining Non-Blockers

These are optional polish items, not blockers:

- add notebook examples only after the scripted workflow remains the source of
  truth;
- consider a GitHub release/tag after an explicit release-boundary decision;
- add a future monitoring run after complete May 2026 month-end data is
  available;
- consider a short project screenshot or generated diagram later if the GitHub
  page needs more visual orientation.

## Decision

Treat milestone 2 as presentation-ready for GitHub portfolio purposes, with the
current claim boundary intact.

The next project direction should be a user-level decision:

- create a formal milestone tag/release;
- start milestone 3;
- wait for fresh forward-monitoring data;
- pause the project in its current public-ready state.
