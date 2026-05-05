import pandas as pd

from macro_regime_portfolio_lab.fresh_forward import (
    FreshForwardMonitoringConfig,
    FrozenMonitoringRule,
    build_pending_signal_rows,
    monitoring_evidence_status,
    parse_fresh_forward_monitoring_config,
    run_fresh_forward_monitoring,
)


def test_parse_fresh_forward_monitoring_config_freezes_rule() -> None:
    config = parse_fresh_forward_monitoring_config(
        {
            "boundary": {
                "last_inspected_signal": "2026-03-31",
                "first_monitoring_signal": "2026-04-30",
            },
            "frozen_rule": {
                "switch_score_buffer": 0.50,
                "min_regime_history": 12,
                "top_n": 3,
                "max_monthly_turnover": 0.15,
                "turnover_metric_warmup_months": 12,
                "fallback_asset": "SHY",
                "cost_bps": 5.0,
            },
            "warnings": {
                "turnover_spike": 0.15,
                "turnover_drift_6m_average": 0.10,
                "drawdown": -0.15,
                "cumulative_equal_weight_lag": -0.10,
                "cumulative_shy_lag": -0.10,
                "repeated_benchmark_lag_months": 6,
            },
        }
    )

    assert config.first_monitoring_signal == pd.Timestamp("2026-04-30")
    assert config.frozen_rule.top_n == 3
    assert config.frozen_rule.max_monthly_turnover == 0.15


def test_monitoring_records_pending_signal_without_completed_return() -> None:
    dates = pd.date_range("2026-01-31", periods=4, freq="ME")
    features = pd.DataFrame({"regime": ["same"] * 4}, index=dates)
    next_returns = pd.DataFrame(
        {
            "SPY": [0.01, 0.01, 0.01],
            "TLT": [0.00, 0.00, 0.00],
            "SHY": [0.001, 0.001, 0.001],
        },
        index=dates[:3],
    )
    config = monitoring_config_for_tests()

    result = run_fresh_forward_monitoring(features, next_returns, config)

    assert result.completed_returns.empty
    assert result.boundary["completed_monitoring_rows"] == 0
    assert result.boundary["pending_signal_rows"] == 1
    assert result.pending_signals.loc[0, "signal_date"] == pd.Timestamp("2026-04-30")
    assert result.metrics.loc[0, "status"] == "no_completed_forward_monitoring_returns"
    assert "data_freshness_warning" in result.warnings["warning"].tolist()


def test_monitoring_does_not_backfill_pre_boundary_returns() -> None:
    dates = pd.date_range("2026-01-31", periods=4, freq="ME")
    features = pd.DataFrame({"regime": ["same"] * 4}, index=dates)
    next_returns = pd.DataFrame(
        {
            "SPY": [0.01, 0.01, 0.01, 0.02],
            "TLT": [0.00, 0.00, 0.00, 0.00],
            "SHY": [0.001, 0.001, 0.001, 0.001],
        },
        index=dates,
    )
    config = monitoring_config_for_tests()

    result = run_fresh_forward_monitoring(features, next_returns, config)

    assert list(result.completed_returns.index) == [pd.Timestamp("2026-04-30")]
    assert result.boundary["completed_monitoring_rows"] == 1
    assert result.pending_signals.empty


def test_pending_signal_rows_exclude_completed_monitoring_rows() -> None:
    dates = pd.date_range("2026-01-31", periods=4, freq="ME")
    features = pd.DataFrame({"regime": ["same"] * 4}, index=dates)
    next_returns = pd.DataFrame(
        {
            "SPY": [0.01, 0.01, 0.01, 0.02],
            "TLT": [0.00, 0.00, 0.00, 0.00],
            "SHY": [0.001, 0.001, 0.001, 0.001],
        },
        index=dates,
    )
    completed = pd.DataFrame(index=[pd.Timestamp("2026-04-30")])
    pending = build_pending_signal_rows(
        features=features,
        next_returns=next_returns,
        config=monitoring_config_for_tests(),
        completed_returns=completed,
    )

    assert pending.empty


def test_monitoring_evidence_status_lanes() -> None:
    assert monitoring_evidence_status(0) == "no_completed_forward_monitoring_returns"
    assert monitoring_evidence_status(5) == "anecdotal_forward_observations"
    assert monitoring_evidence_status(11) == "early_monitoring_evidence"
    assert (
        monitoring_evidence_status(12)
        == "useful_forward_monitoring_sample_not_robustness_proof"
    )


def monitoring_config_for_tests() -> FreshForwardMonitoringConfig:
    return FreshForwardMonitoringConfig(
        last_inspected_signal=pd.Timestamp("2026-03-31"),
        first_monitoring_signal=pd.Timestamp("2026-04-30"),
        frozen_rule=FrozenMonitoringRule(
            switch_score_buffer=0.50,
            min_regime_history=1,
            top_n=1,
            max_monthly_turnover=0.15,
            turnover_metric_warmup_months=0,
            fallback_asset="SHY",
            cost_bps=5.0,
        ),
        warning_thresholds={
            "turnover_spike": 0.15,
            "turnover_drift_6m_average": 0.10,
            "drawdown": -0.15,
            "cumulative_equal_weight_lag": -0.10,
            "cumulative_shy_lag": -0.10,
            "repeated_benchmark_lag_months": 6,
        },
    )
