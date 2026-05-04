# MRPL-016 - Add Robustness Review Suite

- Owner role: Quant Researcher / Data Engineer
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `docs/robustness-review.md`

## Scope

Add a small robustness review for the post-MRPL-014 regime diagnostic before any
public performance language is strengthened.

The goal is not to optimize the strategy. The goal is to test whether the
stronger diagnostic result survives basic robustness checks.

## Acceptance Criteria

- Add subperiod or rolling-window metrics for the default diagnostic setting.
- Add stress-period attribution for major drawdown or macro-regime periods.
- Add a simple uncertainty check for the Sharpe difference, such as bootstrap or
  block-bootstrap diagnostics.
- Add at least one additional simple benchmark beyond equal weight.
- Review whether 0.20 and 0.50 switch-buffer settings remain credible outside a
  full-sample sensitivity ranking.
- Keep conclusions diagnostic and avoid outperformance claims.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
