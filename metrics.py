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


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in DATE_COLS:
        df[col] = pd.to_datetime(df[col])
    return df


def win_rate(df: pd.DataFrame) -> float:
    closed = df[df["status"].isin(["closed_won", "closed_lost"])]
    if closed.empty:
        return 0.0
    won = (closed["status"] == "closed_won").sum()
    return round(won / len(closed) * 100, 1)


def win_rate_by_source(df: pd.DataFrame) -> pd.DataFrame:
    closed = df[df["status"].isin(["closed_won", "closed_lost"])]
    grouped = closed.groupby("source")["status"].apply(
        lambda s: round((s == "closed_won").mean() * 100, 1)
    )
    return grouped.reset_index(name="win_rate_pct")


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
    qualified_opps = df[df["stage"].isin(OPEN_STAGES_ORDER) & (df["status"] == "open")]
    n_qualified = len(qualified_opps)
    deal_size = avg_deal_size(df)
    wr = win_rate(df) / 100
    cycle = avg_sales_cycle_days(df)
    if cycle == 0:
        return 0.0
    return round((n_qualified * deal_size * wr) / cycle, 2)


def open_pipeline_by_stage(df: pd.DataFrame) -> pd.DataFrame:
    open_deals = df[df["status"] == "open"]
    grouped = open_deals.groupby("stage").agg(
        deal_count=("deal_id", "count"), total_amount=("amount", "sum")
    )
    grouped = grouped.reindex(OPEN_STAGES_ORDER).fillna(0)
    return grouped.reset_index()


def coverage_ratio(df: pd.DataFrame, quota: float) -> float:
    open_amount = df[df["status"] == "open"]["amount"].sum()
    if quota == 0:
        return 0.0
    return round(open_amount / quota, 2)


def stalled_deals(df: pd.DataFrame, as_of: datetime = None) -> pd.DataFrame:
    as_of = as_of or datetime.today()
    open_deals = df[df["status"] == "open"].copy()
    open_deals["days_since_activity"] = (as_of - open_deals["last_activity_date"]).dt.days
    return open_deals[open_deals["days_since_activity"] >= STALE_DAYS_THRESHOLD].sort_values(
        "days_since_activity", ascending=False
    )


def single_threaded_deals(df: pd.DataFrame, min_amount: float = 25000) -> pd.DataFrame:
    open_deals = df[df["status"] == "open"]
    return open_deals[(open_deals["contacts_engaged"] <= 1) & (open_deals["amount"] >= min_amount)]


def build_metrics_summary(df: pd.DataFrame, quota: float) -> dict:
    """Empacota tudo num dict compacto pronto pra virar contexto pro Claude."""
    return {
        "win_rate_pct": win_rate(df),
        "win_rate_by_source": win_rate_by_source(df).to_dict(orient="records"),
        "avg_deal_size": avg_deal_size(df),
        "avg_sales_cycle_days": avg_sales_cycle_days(df),
        "pipeline_velocity_per_day": pipeline_velocity(df),
        "open_pipeline_by_stage": open_pipeline_by_stage(df).to_dict(orient="records"),
        "coverage_ratio": coverage_ratio(df, quota),
        "quota": quota,
        "stalled_deals": stalled_deals(df)[
            ["deal_name", "stage", "amount", "days_since_activity"]
        ].to_dict(orient="records"),
        "single_threaded_deals": single_threaded_deals(df)[
            ["deal_name", "stage", "amount", "contacts_engaged"]
        ].to_dict(orient="records"),
    }
