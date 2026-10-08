"""
charts.py
Gráficos PNG do relatório (matplotlib). Cada função recebe dados já calculados
e devolve o caminho do arquivo gerado.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
SERIES = "#2a78d6"
REFERENCE = "#8a8984"


def brl(value: float) -> str:
    """R$ 1.234.567 (sem centavos)."""
    return "R$ " + f"{value:,.0f}".replace(",", ".")


def pct(value: float) -> str:
    """75,0% (vírgula decimal)."""
    return f"{value:.1f}%".replace(".", ",")


def _new_figure(height: float):
    fig, ax = plt.subplots(figsize=(8, height), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=9, length=0)
    return fig, ax


def _title(ax, title: str, subtitle: str):
    ax.set_title(subtitle, loc="left", fontsize=9, color=TEXT_SECONDARY, pad=10)
    ax.annotate(title, (0, 1), xycoords="axes fraction", xytext=(0, 26), textcoords="offset points",
                fontsize=12, weight="bold", color=TEXT_PRIMARY)


def _save(fig, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def _hbar(ax, labels: list, values: list):
    # Primeiro item no topo
    positions = list(range(len(labels)))[::-1]
    ax.barh(positions, values, height=0.6, color=SERIES, edgecolor=SURFACE, linewidth=2)
    ax.set_yticks(positions, labels, color=TEXT_PRIMARY)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    return positions


def pipeline_by_stage_chart(stages: list, path: Path) -> Path:
    labels = [s["stage"] for s in stages]
    amounts = [s["total_amount"] for s in stages]
    fig, ax = _new_figure(0.5 * len(labels) + 1.6)
    positions = _hbar(ax, labels, amounts)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: brl(v)))
    for pos, stage in zip(positions, stages):
        ax.text(
            stage["total_amount"], pos, f"  {brl(stage['total_amount'])} · {stage['deal_count']} neg.",
            va="center", fontsize=8.5, color=TEXT_SECONDARY,
        )
    ax.set_xlim(0, max(amounts + [1]) * 1.35)
    _title(ax, "Pipeline aberto por estágio", "Valor total e número de negócios abertos")
    return _save(fig, path)


def win_rate_by_source_chart(sources: list, path: Path) -> Path:
    sources = sorted(sources, key=lambda s: s["win_rate_pct"], reverse=True)
    labels = [s["source"] for s in sources]
    rates = [s["win_rate_pct"] for s in sources]
    fig, ax = _new_figure(0.5 * len(labels) + 1.6)
    positions = _hbar(ax, labels, rates)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    for pos, source in zip(positions, sources):
        ax.text(
            source["win_rate_pct"], pos,
            f"  {pct(source['win_rate_pct'])} ({source['won_deals']}/{source['closed_deals']})",
            va="center", fontsize=8.5, color=TEXT_SECONDARY,
        )
    ax.set_xlim(0, 115)
    _title(ax, "Win rate por fonte", "Ganhos / negócios fechados — amostras pequenas são instáveis")
    return _save(fig, path)


def _trend(dates: list, values: list, path: Path, title: str, subtitle: str, fmt, references=()):
    fig, ax = _new_figure(3.2)
    ax.plot(dates, values, color=SERIES, linewidth=2, marker="o", markersize=6,
            markeredgecolor=SURFACE, markeredgewidth=2)
    for value, label in references:
        ax.axhline(value, color=REFERENCE, linewidth=1, linestyle="--")
        ax.text(dates[0], value, f" {label}", va="bottom", fontsize=8, color=TEXT_SECONDARY)
    ax.annotate(fmt(values[-1]), (dates[-1], values[-1]), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=9, color=TEXT_PRIMARY)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt(v)))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_ylim(bottom=0, top=max(list(values) + [v for v, _ in references]) * 1.25)
    _title(ax, title, subtitle)
    return _save(fig, path)


def pipeline_trend_chart(history: list, path: Path) -> Path:
    dates = [d for d, _ in history]
    values = [s["open_pipeline_amount"] for _, s in history]
    return _trend(dates, values, path, "Evolução do pipeline aberto",
                  "Valor aberto em cada relatório", brl)


def coverage_trend_chart(history: list, path: Path) -> Path:
    dates = [d for d, _ in history]
    values = [s["coverage_ratio"] for _, s in history]
    return _trend(dates, values, path, "Evolução da cobertura",
                  "Pipeline aberto ÷ meta (referência saudável: 3x)",
                  lambda v: f"{v:.1f}x".replace(".", ","), references=[(1, "meta"), (3, "3x")])


def build_charts(summary: dict, history: list, out_dir: Path) -> list:
    """Gera todos os gráficos aplicáveis e devolve [(título, caminho)]."""
    charts = [
        ("Pipeline aberto por estágio",
         pipeline_by_stage_chart(summary["open_pipeline_by_stage"], out_dir / "pipeline_por_estagio.png")),
    ]
    if summary["win_rate_by_source"]:
        charts.append(("Win rate por fonte",
                       win_rate_by_source_chart(summary["win_rate_by_source"], out_dir / "win_rate_por_fonte.png")))
    if len(history) >= 2:
        charts.append(("Evolução do pipeline aberto",
                       pipeline_trend_chart(history, out_dir / "evolucao_pipeline.png")))
        charts.append(("Evolução da cobertura",
                       coverage_trend_chart(history, out_dir / "evolucao_cobertura.png")))
    return charts
