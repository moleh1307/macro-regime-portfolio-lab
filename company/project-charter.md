# Project Charter: Macro Regime Portfolio Lab

## Purpose

Build a serious, reproducible quant research repo around macro-regime-aware ETF allocation using free public data.

## Audience

- Primary: GitHub portfolio / quant credibility.
- Secondary: serious personal research lab.

## Milestone 1

Reproducible data pipeline plus baseline backtest framework, ending with one simple baseline report.

Milestone 1 explicitly does not attempt to prove outperformance.

## Scope Boundaries

- Use free public data with no API keys by default.
- Data sources: `yfinance` for ETF prices and FRED/public sources for macro series.
- Cache raw data and write source manifests.
- Research/backtesting only.
- No live trading, no execution, no brokerage integration.
- Python stack: `uv`, pandas first, scikit-learn/statsmodels later, notebooks plus CLI scripts.
- Start with a simple custom backtester unless a stronger reason for `vectorbt` appears.

## V0 ETF Universe

SPY, QQQ, IWM, EFA, EEM, TLT, IEF, GLD, DBC, VNQ, UUP, SHY.

## Project-Shape Inference

- Project shape: reproducible public quant research repo with later regime-model extensions.
- What makes success hard: avoiding overclaimed backtests, keeping data provenance inspectable, and separating baseline infrastructure from strategy conclusions.
- Main failure modes: lookahead bias, survivorship/availability ambiguity, unverified data revisions, weak README claims, and premature performance marketing.
- Evidence/artifacts that matter: source manifests, reproducible CLI runs, tests for backtest logic, generated baseline report, clear caveats.
- Roles/disciplines needed: Founder/Chief of Staff, Quant Researcher, Data Engineer, Research Engineer, Replication QA.
- Initial operating mode: build.
- Confidence lanes needed: methodology claims and performance claims must be labeled conservatively until verified.
- Verification/adversarial gates: local tests, schema/manifest checks, baseline report review, later backtest bias review.
- What should not be overbuilt: no live trading stack, no large dashboard, no complex ML regime model before the data/backtest foundation is reliable.

## Related Projects

- Existing separate project: [[portfoliolab]] / `https://github.com/moleh1307/portfoliolab`
- This project is standalone and must not merge with or replace Portfoliolab unless Melih later decides that explicitly.
