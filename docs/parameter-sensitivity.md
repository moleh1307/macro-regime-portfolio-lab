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

The grid produced 20 rows: 5 switch-score buffers by 4 transaction-cost assumptions.

Main findings:

- every tested regime-diagnostic setting had lower net Sharpe than equal weight;
- best regime-diagnostic net Sharpe was 0.6633 at buffer 0.00 and 0 bps cost;
- equal-weight net Sharpe at 0 bps was 0.6903;
- increasing the switch-score buffer usually reduced turnover but did not reliably improve risk-adjusted diagnostics;
- the 0.50 buffer had the lowest average turnover, 0.0128, but worse drawdown than equal weight.

This confirms the current allocation rule is fragile. Do not tune the buffer based on this grid. The next useful work is to improve the regime definition or add a stronger benchmark/evaluation split, not to optimize the switch buffer.
