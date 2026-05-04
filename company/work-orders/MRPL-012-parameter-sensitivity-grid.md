# MRPL-012 - Run Parameter Sensitivity Grid

- Owner role: Quant Researcher / Research Engineer
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `artifacts/reports/parameter_sensitivity.csv`

## Scope

Run a small diagnostic sensitivity grid before accepting any allocation rule as the milestone default:

- vary switch-score buffer values;
- vary transaction-cost assumptions;
- compare net Sharpe, net return, max drawdown, and turnover;
- keep conclusions diagnostic only.

## Acceptance Criteria

- Add a reproducible sensitivity script or function.
- Generate a compact CSV/table artifact.
- Document which settings look fragile versus stable.
- Do not tune the default purely to maximize historical performance.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
