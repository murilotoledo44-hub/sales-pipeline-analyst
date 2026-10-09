"""Testes dos cálculos determinísticos usando o CSV de exemplo."""

import sys
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import metrics  # noqa: E402

SAMPLE = ROOT / "data" / "sample_pipeline.csv"


@pytest.fixture(scope="module")
def df():
    return metrics.load_data(SAMPLE)


def test_win_rate(df):
    # 8 ganhos de 15 fechados
    assert metrics.win_rate(df) == 53.3


def test_win_rate_by_source_includes_sample_size(df):
    by_source = metrics.win_rate_by_source(df).set_index("source")
    assert by_source.loc["Inbound", "closed_deals"] == 4
    assert by_source.loc["Inbound", "win_rate_pct"] == 75.0
    assert by_source.loc["Outbound", "closed_deals"] == 8
    assert by_source.loc["Outbound", "win_rate_pct"] == 37.5
    assert by_source.loc["Referral", "closed_deals"] == 3


def test_avg_deal_size_and_cycle(df):
    assert metrics.avg_deal_size(df) == 39375.0
    assert metrics.avg_sales_cycle_days(df) == 90.0


def test_coverage_ratio(df):
    assert metrics.coverage_ratio(df, 250000) == 1.96
    assert metrics.coverage_ratio(df, 0) == 0.0


def test_snapshot_date_is_latest_activity(df):
    assert metrics.snapshot_date(df) == datetime(2026, 9, 17)


def test_stalled_deals_use_snapshot_date_by_default(df):
    stalled = metrics.stalled_deals(df)
    assert list(stalled["deal_name"]) == [
        "Nordic Freight Co",
        "Fintra Payments",
        "Lumen Energy Co",
        "Ironclad Security",
        "BrightPath Retail",
    ]
    assert stalled.iloc[0]["days_since_activity"] == 38


def test_stalled_deals_respects_explicit_as_of(df):
    # Um mês depois, todos os 15 negócios abertos estariam parados
    assert len(metrics.stalled_deals(df, as_of=datetime(2026, 10, 20))) == 15


def test_single_threaded_deals(df):
    names = set(metrics.single_threaded_deals(df)["deal_name"])
    assert names == {
        "Nordic Freight Co",
        "Fintra Payments",
        "Harbor Insurance",
        "Lumen Energy Co",
        "Kestrel Biotech",
    }


def test_build_metrics_summary(df):
    summary = metrics.build_metrics_summary(df, quota=250000)
    assert summary["as_of_date"] == "2026-09-17"
    assert summary["open_deal_count"] == 15
    assert summary["open_pipeline_amount"] == 491000.0
    assert len(summary["stalled_deals"]) == 5


def test_open_pipeline_by_stage_custom_order(df):
    custom = df.copy()
    custom.loc[custom["deal_name"] == "Kestrel Biotech", "stage"] = "Solution Fit"
    stages = metrics.open_pipeline_by_stage(custom, ["Negotiation", "Discovery"])
    assert list(stages["stage"])[:2] == ["Negotiation", "Discovery"]
    assert "Solution Fit" in list(stages["stage"])


def test_data_quality(df):
    quality = metrics.data_quality(df)
    assert quality["total_deals"] == 30
    assert quality["deals_without_source_pct"] == 0.0
    assert quality["open_deals_without_contacts_pct"] == 0.0


def test_summary_caps_listed_deals(df):
    summary = metrics.build_metrics_summary(df, quota=250000, single_thread_min_amount=0)
    assert summary["single_threaded_deal_count"] == 9
    assert len(summary["single_threaded_deals"]) == 9
    assert summary["single_threaded_deals"][0]["deal_name"] == "Nordic Freight Co"
