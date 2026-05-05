from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from macro_regime_portfolio_lab.backtest import calculate_metrics
from macro_regime_portfolio_lab.evaluation import run_regime_walk_forward
from macro_regime_portfolio_lab.robustness import compound_return, max_drawdown
from macro_regime_portfolio_lab.validation import add_validation_benchmarks


@dataclass(frozen=True)
class FrozenMonitoringRule:
    switch_score_buffer: float
    min_regime_history: int
    top_n: int
    max_monthly_turnover: float
    turnover_metric_warmup_months: int
    fallback_asset: str
    cost_bps: float


@dataclass(frozen=True)
class FreshForwardMonitoringConfig:
    last_inspected_signal: pd.Timestamp
    first_monitoring_signal: pd.Timestamp
    frozen_rule: FrozenMonitoringRule
    warning_thresholds: dict[str, float | int]


@dataclass(frozen=True)
class FreshForwardMonitoringResult:
    completed_returns: pd.DataFrame
    metrics: pd.DataFrame
    warnings: pd.DataFrame
    pending_signals: pd.DataFrame
    boundary: dict[str, pd.Timestamp | int | str | None]
    frozen_rule: dict[str, float | int | str]


def parse_fresh_forward_monitoring_config(
    config: dict[str, Any],
) -> FreshForwardMonitoringConfig:
    boundary = config["boundary"]
    rule = config["frozen_rule"]
    return FreshForwardMonitoringConfig(
        last_inspected_signal=pd.Timestamp(boundary["last_inspected_signal"]),
        first_monitoring_signal=pd.Timestamp(boundary["first_monitoring_signal"]),
        frozen_rule=FrozenMonitoringRule(
            switch_score_buffer=float(rule["switch_score_buffer"]),
            min_regime_history=int(rule["min_regime_history"]),
            top_n=int(rule["top_n"]),
            max_monthly_turnover=float(rule["max_monthly_turnover"]),
            turnover_metric_warmup_months=int(rule["turnover_metric_warmup_months"]),
            fallback_asset=str(rule["fallback_asset"]),
            cost_bps=float(rule["cost_bps"]),
        ),
        warning_thresholds={
            key: float(value) if isinstance(value, float) else int(value)
            for key, value in config["warnings"].items()
        },
    )


def run_fresh_forward_monitoring(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: FreshForwardMonitoringConfig,
) -> FreshForwardMonitoringResult:
    completed_next_returns = next_returns.loc[
        next_returns.index >= config.first_monitoring_signal
    ].dropna(how="all")
    completed_full_returns = run_frozen_rule(
        features,
        next_returns,
        config,
    )
    completed_returns = completed_full_returns.loc[
        completed_next_returns.index.intersection(completed_full_returns.index)
    ]

    pending_signals = build_pending_signal_rows(
        features=features,
        next_returns=next_returns,
        config=config,
        completed_returns=completed_returns,
    )
    warnings = build_monitoring_warnings(
        completed_returns=completed_returns,
        pending_signals=pending_signals,
        config=config,
    )
    metrics = summarize_monitoring_metrics(completed_returns)
    boundary = build_monitoring_boundary(
        features=features,
        next_returns=next_returns,
        completed_returns=completed_returns,
        pending_signals=pending_signals,
        config=config,
    )
    return FreshForwardMonitoringResult(
        completed_returns=completed_returns,
        metrics=metrics,
        warnings=warnings,
        pending_signals=pending_signals,
        boundary=boundary,
        frozen_rule=frozen_rule_dict(config.frozen_rule),
    )


def run_frozen_rule(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: FreshForwardMonitoringConfig,
) -> pd.DataFrame:
    rule = config.frozen_rule
    result = run_regime_walk_forward(
        features,
        next_returns,
        min_regime_history=rule.min_regime_history,
        top_n=rule.top_n,
        fallback_asset=rule.fallback_asset,
        cost_bps=rule.cost_bps,
        switch_score_buffer=rule.switch_score_buffer,
        max_monthly_turnover=rule.max_monthly_turnover,
    )
    return add_validation_benchmarks(
        result.returns,
        next_returns,
        cost_bps=rule.cost_bps,
        fallback_asset=rule.fallback_asset,
    )


def build_pending_signal_rows(
    *,
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: FreshForwardMonitoringConfig,
    completed_returns: pd.DataFrame,
) -> pd.DataFrame:
    pending_index = features.loc[features.index >= config.first_monitoring_signal].index
    completed_index = completed_returns.index
    pending_index = pending_index.difference(completed_index)
    if pending_index.empty:
        return empty_pending_signals_frame()

    next_returns_with_pending = next_returns.reindex(next_returns.index.union(pending_index))
    pending_full_returns = run_frozen_rule(
        features=features,
        next_returns=next_returns_with_pending,
        config=config,
    )
    pending = pending_full_returns.loc[pending_index.intersection(pending_full_returns.index)]
    if pending.empty:
        return empty_pending_signals_frame()
    return pd.DataFrame(
        {
            "signal_date": pending.index,
            "regime": pending["regime"].to_numpy(),
            "selected_assets": pending["selected_assets"].to_numpy(),
            "strategy_turnover": pending["strategy_turnover"].to_numpy(),
            "strategy_cost": pending["strategy_cost"].to_numpy(),
            "status": "pending_completed_next_month_return",
        }
    )


def summarize_monitoring_metrics(completed_returns: pd.DataFrame) -> pd.DataFrame:
    if completed_returns.empty:
        return pd.DataFrame(
            [
                {
                    "monitoring_rows": 0,
                    "latest_signal_date": pd.NaT,
                    "latest_realized_return_date": pd.NaT,
                    "strategy_cumulative_return": pd.NA,
                    "equal_weight_cumulative_return": pd.NA,
                    "static_60_40_cumulative_return": pd.NA,
                    "shy_cumulative_return": pd.NA,
                    "strategy_max_drawdown": pd.NA,
                    "average_monthly_turnover": pd.NA,
                    "status": "no_completed_forward_monitoring_returns",
                }
            ]
        )

    strategy_metrics = calculate_metrics(completed_returns["strategy_return_net"])
    return pd.DataFrame(
        [
            {
                "monitoring_rows": len(completed_returns),
                "latest_signal_date": completed_returns.index.max(),
                "latest_realized_return_date": completed_returns.index.max(),
                "strategy_cumulative_return": compound_return(
                    completed_returns["strategy_return_net"]
                ),
                "equal_weight_cumulative_return": compound_return(
                    completed_returns["equal_weight_return_net"]
                ),
                "static_60_40_cumulative_return": compound_return(
                    completed_returns["static_60_40_return_net"]
                ),
                "shy_cumulative_return": compound_return(completed_returns["shy_return_net"]),
                "strategy_max_drawdown": strategy_metrics["max_drawdown"],
                "average_monthly_turnover": float(
                    completed_returns["strategy_turnover"].mean()
                ),
                "status": monitoring_evidence_status(len(completed_returns)),
            }
        ]
    )


def build_monitoring_warnings(
    *,
    completed_returns: pd.DataFrame,
    pending_signals: pd.DataFrame,
    config: FreshForwardMonitoringConfig,
) -> pd.DataFrame:
    warnings = []
    thresholds = config.warning_thresholds
    for signal_date, row in completed_returns.iterrows():
        if row["strategy_turnover"] > thresholds["turnover_spike"]:
            warnings.append(
                warning_record(
                    signal_date=signal_date,
                    warning="turnover_spike",
                    value=row["strategy_turnover"],
                    threshold=thresholds["turnover_spike"],
                )
            )

    if len(completed_returns) >= 6:
        turnover_6m = completed_returns["strategy_turnover"].rolling(6).mean()
        turnover_drift = turnover_6m[
            turnover_6m > thresholds["turnover_drift_6m_average"]
        ]
        for signal_date, value in turnover_drift.items():
            warnings.append(
                warning_record(
                    signal_date=signal_date,
                    warning="turnover_drift",
                    value=value,
                    threshold=thresholds["turnover_drift_6m_average"],
                )
            )

    if not completed_returns.empty:
        strategy_drawdown = max_drawdown(completed_returns["strategy_return_net"])
        if strategy_drawdown < thresholds["drawdown"]:
            warnings.append(
                warning_record(
                    signal_date=completed_returns.index.max(),
                    warning="drawdown_warning",
                    value=strategy_drawdown,
                    threshold=thresholds["drawdown"],
                )
            )
        strategy_cumulative = compound_return(completed_returns["strategy_return_net"])
        equal_weight_lag = strategy_cumulative - compound_return(
            completed_returns["equal_weight_return_net"]
        )
        shy_lag = strategy_cumulative - compound_return(completed_returns["shy_return_net"])
        if equal_weight_lag < thresholds["cumulative_equal_weight_lag"]:
            warnings.append(
                warning_record(
                    signal_date=completed_returns.index.max(),
                    warning="equal_weight_lag",
                    value=equal_weight_lag,
                    threshold=thresholds["cumulative_equal_weight_lag"],
                )
            )
        if shy_lag < thresholds["cumulative_shy_lag"]:
            warnings.append(
                warning_record(
                    signal_date=completed_returns.index.max(),
                    warning="defensive_lag",
                    value=shy_lag,
                    threshold=thresholds["cumulative_shy_lag"],
                )
            )
        repeated_months = int(thresholds["repeated_benchmark_lag_months"])
        if len(completed_returns) >= repeated_months:
            trails_both = (
                completed_returns["strategy_return_net"]
                < completed_returns["equal_weight_return_net"]
            ) & (
                completed_returns["strategy_return_net"]
                < completed_returns["shy_return_net"]
            )
            if trails_both.tail(repeated_months).all():
                warnings.append(
                    warning_record(
                        signal_date=completed_returns.index.max(),
                        warning="repeated_benchmark_lag",
                        value=repeated_months,
                        threshold=repeated_months,
                    )
                )

    if not pending_signals.empty:
        for signal_date in pending_signals["signal_date"]:
            warnings.append(
                warning_record(
                    signal_date=signal_date,
                    warning="data_freshness_warning",
                    value="pending_completed_next_month_return",
                    threshold="complete_next_month_price_observation",
                )
            )
    return pd.DataFrame.from_records(warnings, columns=warning_columns())


def build_monitoring_boundary(
    *,
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    completed_returns: pd.DataFrame,
    pending_signals: pd.DataFrame,
    config: FreshForwardMonitoringConfig,
) -> dict[str, pd.Timestamp | int | str | None]:
    return {
        "last_inspected_signal": config.last_inspected_signal,
        "first_monitoring_signal": config.first_monitoring_signal,
        "latest_feature_date": features.index.max() if not features.empty else None,
        "latest_completed_next_return_signal": (
            next_returns.dropna(how="all").index.max() if not next_returns.empty else None
        ),
        "completed_monitoring_rows": len(completed_returns),
        "pending_signal_rows": len(pending_signals),
        "latest_completed_monitoring_signal": (
            completed_returns.index.max() if not completed_returns.empty else None
        ),
        "latest_pending_signal": (
            pd.Timestamp(pending_signals["signal_date"].max())
            if not pending_signals.empty
            else None
        ),
    }


def monitoring_evidence_status(row_count: int) -> str:
    if row_count == 0:
        return "no_completed_forward_monitoring_returns"
    if row_count <= 5:
        return "anecdotal_forward_observations"
    if row_count <= 11:
        return "early_monitoring_evidence"
    return "useful_forward_monitoring_sample_not_robustness_proof"


def frozen_rule_dict(rule: FrozenMonitoringRule) -> dict[str, float | int | str]:
    return {
        "switch_score_buffer": rule.switch_score_buffer,
        "min_regime_history": rule.min_regime_history,
        "top_n": rule.top_n,
        "max_monthly_turnover": rule.max_monthly_turnover,
        "turnover_metric_warmup_months": rule.turnover_metric_warmup_months,
        "fallback_asset": rule.fallback_asset,
        "cost_bps": rule.cost_bps,
    }


def warning_record(
    *,
    signal_date: pd.Timestamp,
    warning: str,
    value: object,
    threshold: object,
) -> dict[str, object]:
    return {
        "signal_date": signal_date,
        "warning": warning,
        "value": value,
        "threshold": threshold,
        "status": "diagnostic_warning",
    }


def warning_columns() -> list[str]:
    return ["signal_date", "warning", "value", "threshold", "status"]


def empty_pending_signals_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "signal_date",
            "regime",
            "selected_assets",
            "strategy_turnover",
            "strategy_cost",
            "status",
        ]
    )
