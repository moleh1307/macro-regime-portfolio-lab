# Turnover Stability Review

## Purpose

MRPL-022 reviews the MRPL-021 turnover-stability result and decides how to treat
the second-cycle diagnostic branch.

This review preserves two boundaries:

- MRPL-018 remains the first locked validation result.
- MRPL-021 is a `post-holdout-review diagnostic run`, not fresh independent
  validation.

## What Improved

MRPL-021 directly addressed the failure mode identified in
`docs/validation-review.md`: the first locked validation run selected a rule
with acceptable research-window average turnover but much higher 2022-forward
turnover.

Turnover comparison:

| Run | Rule | 2022-forward average monthly turnover |
| --- | --- | ---: |
| MRPL-018 locked validation | top_n 4, no monthly turnover cap | 0.2304 |
| MRPL-021 post-holdout-review diagnostic | top_n 3, 0.15 max monthly turnover guard | 0.0435 |

The improvement is meaningful for research credibility. The second-cycle screen
requires candidates to pass hard turnover-stability thresholds inside the
research window before ranking, then applies a max monthly turnover guard during
walk-forward evaluation. This converts turnover from an after-the-fact caveat
into a first-class selection constraint.

The selected MRPL-021 candidate also passed a stricter research-window turnover
profile:

| Metric | Selected value | Hard threshold |
| --- | ---: | ---: |
| average turnover | 0.0595 | 0.10 |
| turnover p90 | 0.1500 | 0.35 |
| turnover p95 | 0.1500 | 0.50 |
| high-turnover month share | 0.0000 | 0.20 |
| turnover volatility | 0.0721 | 0.18 |
| rolling 12m average turnover max | 0.1389 | 0.18 |

## What Did Not Improve

The second-cycle diagnostic should not be treated as a stronger performance
result.

Post-holdout-review metrics:

| Strategy | Net annualized return | Net volatility | Net Sharpe | Max drawdown | Average turnover |
| --- | ---: | ---: | ---: | ---: | ---: |
| regime_diagnostic_net | 0.0563 | 0.0687 | 0.8194 | -0.1019 | 0.0435 |
| equal_weight_net | 0.0831 | 0.1005 | 0.8266 | -0.1487 | 0.0000 |
| static_60_40_net | 0.0446 | 0.1397 | 0.3194 | -0.2069 | |
| shy_net | 0.0237 | 0.0214 | 1.1053 | -0.0358 | |

The second-cycle rule no longer beats equal weight on net Sharpe in the
2022-forward diagnostic slice. It still beats static 60/40 on Sharpe and
drawdown, but it does not clear SHY. Its strongest visible improvement is lower
drawdown versus equal weight and static 60/40, not return or Sharpe dominance.

The bootstrap comparison also remains non-claim-grade:

| Benchmark | Observed Sharpe difference | Bootstrap p05 | Bootstrap p95 | Share positive |
| --- | ---: | ---: | ---: | ---: |
| equal_weight_net | -0.0071 | -0.4420 | 0.8301 | 0.6900 |
| static_60_40_net | 0.5001 | 0.1761 | 1.1751 | 0.9920 |
| shy_net | -0.2858 | -1.2618 | 0.5044 | 0.2610 |

This supports a narrow statement: the turnover-stability protocol reduced the
known turnover failure mode. It does not support a robust outperformance claim.

## Methodology Decision

Treat the MRPL-021 branch as the current research-branch default for future
methodology work, but not as a validated strategy.

Rationale:

- it fixes the most concrete behavioral defect from MRPL-018;
- it uses predeclared research-window diagnostics before touching the
  post-holdout-review period;
- it gives up some return/Sharpe performance in exchange for much more stable
  allocation behavior;
- it still fails the full benchmark-panel hurdle because SHY remains stronger
  on Sharpe and drawdown;
- the 2022-forward period has already been inspected, so the branch cannot
  become fresh validation evidence.

Practical consequence: future research should start from the turnover-stable
protocol mechanics unless there is a documented reason to compare against the
MRPL-018 branch. Public docs should keep both results visible: MRPL-018 as the
first locked partial validation and MRPL-021 as a post-holdout-review diagnostic
repair of the turnover failure mode.

## Next Methodology Work

The next work should not tune parameters on the 2022-forward result. The clean
next step is to define a fresh-data-forward monitoring protocol.

Candidate scope:

- freeze the current research-branch default configuration from MRPL-021;
- define how newly arriving monthly data after the current cached sample will be
  appended and reviewed;
- track turnover, drawdown, benchmark-relative return, and allocation changes
  without changing the rule after each new month;
- keep a separate monitoring log so future data is not mixed with the already
  inspected 2022-forward period.

This turns the project toward honest forward evidence instead of repeated
post-holdout redesign.

## Claim Boundary

Allowed:

- "The second-cycle protocol reduced the known turnover failure mode."
- "The turnover-stable branch is a more credible research default for future
  monitoring."
- "The evidence remains diagnostic and requires fresh forward data."

Not allowed:

- robust outperformance;
- validated strategy;
- investment-ready allocation;
- fresh holdout result;
- alpha claim.

## Decision

Adopt the MRPL-021 turnover-stable branch as the current research branch for
future methodology work, while preserving MRPL-018 as the first locked validation
result and MRPL-021 as a post-holdout-review diagnostic.

The next useful task is to design a fresh-data-forward monitoring protocol.
