"""
metrics.py
Cálculos determinísticos de pipeline a partir de um CSV de CRM.
Nenhuma chamada de IA acontece aqui — só matemática de verdade.
"""

from datetime import datetime
import pandas as pd

DATE_COLS = ["created_date", "close_date", "last_activity_date"]
OPEN_STAGES_ORDER = ["Discovery", "Qualification", "Evaluation", "Proposal", "Negotiation"]
STALE_DAYS_THRESHOLD = 14
CURRENCY = "USD"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in DATE_COLS:
        df[col] = pd.to_datetime(df[col])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["contacts_engaged"] = pd.to_numeric(df["contacts_engaged"], errors="coerce").fillna(0)
    return df


def win_rate(df: pd.DataFrame) -> float:
    closed = df[df["status"].isin(["closed_won", "closed_lost"])]
    if closed.empty:
        return 0.0
    won = (closed["status"] == "closed_won").sum()
    return round(won / len(closed) * 100, 1)


def win_rate_by_source(df: pd.DataFrame) -> pd.DataFrame:
    """Win rate por fonte, com o tamanho da amostra (n) pra evitar conclusões em cima de ruído."""
    closed = df[df["status"].isin(["closed_won", "closed_lost"])]
    grouped = closed.groupby("source")["status"].agg(
        closed_deals="count", won_deals=lambda s: (s == "closed_won").sum()
    )
    grouped["win_rate_pct"] = (grouped["won_deals"] / grouped["closed_deals"] * 100).round(1)
    return grouped.reset_index()


def avg_deal_size(df: pd.DataFrame) -> float:
    won = df[df["status"] == "closed_won"]
    if won.empty:
        return 0.0
    return round(won["amount"].mean(), 2)


def avg_sales_cycle_days(df: pd.DataFrame) -> float:
    won = df[df["status"] == "closed_won"].copy()
    if won.empty:
        return 0.0
    won["cycle_days"] = (won["close_date"] - won["created_date"]).dt.days
    return round(won["cycle_days"].mean(), 1)


def pipeline_velocity(df: pd.DataFrame) -> float:
    """Pipeline Velocity = (Qualified Opps x Avg Deal Size x Win Rate) / Sales Cycle Length"""
    qualified_opps = df[df["status"] == "open"]
    n_qualified = len(qualified_opps)
    deal_size = avg_deal_size(df)
    wr = win_rate(df) / 100
    cycle = avg_sales_cycle_days(df)
    if cycle == 0:
        return 0.0
    return round((n_qualified * deal_size * wr) / cycle, 2)


def open_pipeline_by_stage(df: pd.DataFrame, stage_order: list = None) -> pd.DataFrame:
    open_deals = df[df["status"] == "open"]
    grouped = open_deals.groupby("stage").agg(
        deal_count=("deal_id", "count"), total_amount=("amount", "sum")
    )
    order = list(stage_order or OPEN_STAGES_ORDER)
    # Estágios que não estão na ordem conhecida (ex.: pipeline customizado) vão pro fim
    order += [stage for stage in grouped.index if stage not in order]
    grouped = grouped.reindex(order).fillna(0).astype({"deal_count": int})
    grouped.index.name = "stage"
    return grouped.reset_index()


def coverage_ratio(df: pd.DataFrame, quota: float) -> float:
    open_amount = df[df["status"] == "open"]["amount"].sum()
    if quota == 0:
        return 0.0
    return round(open_amount / quota, 2)


def snapshot_date(df: pd.DataFrame) -> datetime:
    """Data de referência do extrato: a atividade mais recente registrada no CSV.

    Usar a data de hoje faria um CSV estático (como o de exemplo) envelhecer
    sozinho e marcar todos os negócios como estagnados com o passar das semanas.
    """
    return df["last_activity_date"].max().to_pydatetime()


def stalled_deals(df: pd.DataFrame, as_of: datetime = None) -> pd.DataFrame:
    as_of = as_of or snapshot_date(df)
    open_deals = df[df["status"] == "open"].copy()
    open_deals["days_since_activity"] = (as_of - open_deals["last_activity_date"]).dt.days
    return open_deals[open_deals["days_since_activity"] >= STALE_DAYS_THRESHOLD].sort_values(
        "days_since_activity", ascending=False
    )


def single_threaded_deals(df: pd.DataFrame, min_amount: float = 25000) -> pd.DataFrame:
    open_deals = df[df["status"] == "open"]
    return open_deals[(open_deals["contacts_engaged"] <= 1) & (open_deals["amount"] >= min_amount)]


def data_quality(df: pd.DataFrame, unknown_source: str = "Desconhecida") -> dict:
    """Sinais de dado faltando que distorcem as métricas — o relatório deve citá-los."""
    open_deals = df[df["status"] == "open"]
    total = len(df)

    def pct(n: int, base: int) -> float:
        return round(n / base * 100, 1) if base else 0.0

    return {
        "total_deals": int(total),
        "deals_without_amount_pct": pct(int((df["amount"] <= 0).sum()), total),
        "deals_without_source_pct": pct(
            int((df["source"].isna() | (df["source"] == unknown_source)).sum()), total
        ),
        "open_deals_without_contacts_pct": pct(
            int((open_deals["contacts_engaged"] <= 0).sum()), len(open_deals)
        ),
    }


MAX_LISTED_DEALS = 15


def _top_deals(deals: pd.DataFrame, columns: list) -> list:
    """Os maiores negócios da lista, pra manter o contexto do Claude enxuto."""
    return deals.sort_values("amount", ascending=False).head(MAX_LISTED_DEALS)[columns].to_dict(
        orient="records"
    )


def build_metrics_summary(
    df: pd.DataFrame,
    quota: float,
    as_of: datetime = None,
    stage_order: list = None,
    single_thread_min_amount: float = 25000,
) -> dict:
    """Empacota tudo num dict compacto pronto pra virar contexto pro Claude."""
    as_of = as_of or snapshot_date(df)
    open_deals = df[df["status"] == "open"]
    stalled = stalled_deals(df, as_of=as_of)
    single = single_threaded_deals(df, min_amount=single_thread_min_amount)
    return {
        "currency": CURRENCY,
        "as_of_date": as_of.date().isoformat(),
        "stale_days_threshold": STALE_DAYS_THRESHOLD,
        "open_deal_count": int(len(open_deals)),
        "open_pipeline_amount": float(open_deals["amount"].sum()),
        "win_rate_pct": win_rate(df),
        "win_rate_by_source": win_rate_by_source(df).to_dict(orient="records"),
        "avg_deal_size": avg_deal_size(df),
        "avg_sales_cycle_days": avg_sales_cycle_days(df),
        "pipeline_velocity_per_day": pipeline_velocity(df),
        "open_pipeline_by_stage": open_pipeline_by_stage(df, stage_order).to_dict(orient="records"),
        "coverage_ratio": coverage_ratio(df, quota),
        "quota": quota,
        "stalled_deal_count": int(len(stalled)),
        "stalled_amount": float(stalled["amount"].sum()),
        "stalled_deals": _top_deals(stalled, ["deal_name", "stage", "amount", "days_since_activity"]),
        "single_thread_min_amount": single_thread_min_amount,
        "single_threaded_deal_count": int(len(single)),
        "single_threaded_amount": float(single["amount"].sum()),
        "single_threaded_deals": _top_deals(
            single, ["deal_name", "stage", "amount", "contacts_engaged"]
        ),
        "data_quality": data_quality(df),
    }
