# Parameter Sensitivity Grid

## Purpose

MRPL-012 runs a small diagnostic grid over turnover-control and transaction-cost assumptions.

This grid is not a tuning step. It is a fragility check. The goal is to see whether the diagnostic rule behaves consistently across nearby assumptions before treating any setting as a milestone default.

## Grid

Switch-score buffer values:

- 0.00
- 0.05
- 0.10
- 0.20
- 0.50

Transaction-cost assumptions:

- 0 bps
- 5 bps
- 10 bps
- 25 bps

## Outputs

The script writes:

- `artifacts/reports/parameter_sensitivity.csv`

The table includes:

- net annualized return;
- net volatility;
- net Sharpe;
- max drawdown;
- average turnover;
- matching equal-weight net metrics.

## Interpretation Rules

- Do not pick the best historical row as the default without further validation.
- Treat sensitivity to small buffer changes as fragility.
- Prefer settings that reduce turnover only when they do not materially worsen risk-adjusted diagnostics.
- Keep all conclusions diagnostic until robustness checks exist.

## Observed Result

Post-MRPL-014 update: the grid was regenerated after the stricter growth regime
definition became the milestone default.

The grid produced 20 rows: 5 switch-score buffers by 4 transaction-cost assumptions.

Main findings:

- twelve of twenty tested regime-diagnostic settings beat equal weight on net Sharpe;
- best regime-diagnostic net Sharpe was 0.9821 at buffer 0.50 and 0 bps cost;
- equal-weight net Sharpe at 0 bps was 0.6903;
- the current default row, buffer 0.10 and 5 bps cost, had regime net Sharpe 0.7392 versus equal-weight net Sharpe 0.6901;
- higher buffers reduced turnover and improved risk-adjusted diagnostics in this sample;
- the 0.50 buffer had average monthly turnover 0.0593 and the strongest grid metrics.

This is a promising diagnostic result, but it also creates a parameter-dependence warning. Do not tune the buffer based on this grid. The next useful work is to test subperiod stability, stress-period attribution, uncertainty around Sharpe differences, and additional simple benchmarks before strengthening any public performance language.
