"""Testes da comparação entre relatórios e da geração de gráficos."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import charts  # noqa: E402
import history  # noqa: E402
import metrics  # noqa: E402


@pytest.fixture(scope="module")
def summary():
    df = metrics.load_data(ROOT / "data" / "sample_pipeline.csv")
    return metrics.build_metrics_summary(df, quota=250000)


def test_previous_snapshot_ignores_same_day_and_later(tmp_path, summary):
    history.save_snapshot(tmp_path, "2026-09-28", summary)
    history.save_snapshot(tmp_path, "2026-10-05", summary)
    history.save_snapshot(tmp_path, "2026-10-08", summary)
    past = history.load_history(tmp_path)
    assert [d for d, _ in past] == ["2026-09-28", "2026-10-05", "2026-10-08"]
    assert history.previous_snapshot(past, "2026-10-08")[0] == "2026-10-05"
    assert history.previous_snapshot(past, "2026-09-28") is None


def test_compare_reports_deltas_and_stalled_changes(summary):
    previous = dict(summary, open_pipeline_amount=400000.0, coverage_ratio=1.6)
    previous["stalled_deals"] = [{"deal_name": "Nordic Freight Co"}, {"deal_name": "Old Deal"}]
    result = history.compare(summary, previous, "2026-10-01")

    pipeline = result["metrics"]["open_pipeline_amount"]
    assert pipeline["change"] == 91000.0
    assert pipeline["change_pct"] == 22.8
    assert result["no_longer_stalled_deals"] == ["Old Deal"]
    assert "Fintra Payments" in result["newly_stalled_deals"]
    assert "Nordic Freight Co" not in result["newly_stalled_deals"]


def test_compare_handles_zero_baseline(summary):
    previous = dict(summary, stalled_deal_count=0)
    assert history.compare(summary, previous, "x")["metrics"]["stalled_deal_count"]["change_pct"] is None


def test_build_charts(tmp_path, summary):
    single = charts.build_charts(summary, [("2026-10-08", summary)], tmp_path / "a")
    assert [title for title, _ in single] == ["Pipeline aberto por estágio", "Win rate por fonte"]

    trend = [("2026-10-01", summary), ("2026-10-08", summary)]
    full = charts.build_charts(summary, trend, tmp_path / "b")
    assert len(full) == 4
    assert all(path.exists() and path.stat().st_size > 0 for _, path in full)


def test_number_formats():
    assert charts.usd(1234567) == "$1,234,567"
    assert charts.pct(75) == "75.0%"
