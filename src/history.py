"""
history.py
Guarda um snapshot das métricas a cada execução e compara com o anterior,
pra o relatório falar de tendência e não só da foto do momento.
"""

import json
from pathlib import Path

# Métricas escalares comparadas período a período
TRACKED_METRICS = [
    "open_pipeline_amount",
    "open_deal_count",
    "coverage_ratio",
    "win_rate_pct",
    "avg_deal_size",
    "avg_sales_cycle_days",
    "pipeline_velocity_per_day",
    "stalled_deal_count",
    "stalled_amount",
    "single_threaded_deal_count",
]


def save_snapshot(history_dir: Path, run_date: str, summary: dict) -> Path:
    history_dir.mkdir(parents=True, exist_ok=True)
    path = history_dir / f"metrics_{run_date}.json"
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_history(history_dir: Path) -> list:
    """Snapshots salvos, do mais antigo pro mais recente, como (data, resumo)."""
    if not history_dir.exists():
        return []
    snapshots = []
    for path in sorted(history_dir.glob("metrics_*.json")):
        run_date = path.stem.removeprefix("metrics_")
        snapshots.append((run_date, json.loads(path.read_text(encoding="utf-8"))))
    return snapshots


def previous_snapshot(history: list, run_date: str):
    """O snapshot mais recente anterior a run_date, ou None."""
    earlier = [(d, s) for d, s in history if d < run_date]
    return earlier[-1] if earlier else None


def compare(current: dict, previous: dict, previous_date: str) -> dict:
    """Variação absoluta e percentual de cada métrica acompanhada + mudanças nos estagnados."""
    deltas = {}
    for key in TRACKED_METRICS:
        if key not in current or key not in previous:
            continue
        now, before = current[key], previous[key]
        deltas[key] = {
            "previous": before,
            "current": now,
            "change": round(now - before, 2),
            "change_pct": round((now - before) / before * 100, 1) if before else None,
        }

    current_stalled = {d["deal_name"] for d in current.get("stalled_deals", [])}
    previous_stalled = {d["deal_name"] for d in previous.get("stalled_deals", [])}
    return {
        "previous_as_of_date": previous.get("as_of_date"),
        "previous_report_date": previous_date,
        "metrics": deltas,
        "newly_stalled_deals": sorted(current_stalled - previous_stalled),
        "no_longer_stalled_deals": sorted(previous_stalled - current_stalled),
    }
