"""
hubspot_source.py
Exporta os negócios do HubSpot para o CSV no formato que o metrics.py espera.

Uso:
    export HUBSPOT_ACCESS_TOKEN="pat-..."   # Private App com escopo crm.objects.deals.read
    python src/hubspot_source.py --out data/hubspot_pipeline.csv
"""

import argparse
import csv
import os
from pathlib import Path

import requests

API = "https://api.hubapi.com"
DEAL_PROPERTIES = [
    "dealname",
    "dealstage",
    "pipeline",
    "amount",
    "createdate",
    "closedate",
    "notes_last_updated",
    "num_associated_contacts",
    "hs_analytics_source",
]
CSV_COLUMNS = [
    "deal_id",
    "deal_name",
    "stage",
    "status",
    "amount",
    "source",
    "created_date",
    "close_date",
    "last_activity_date",
    "contacts_engaged",
]
SOURCE_LABELS = {
    "ORGANIC_SEARCH": "Organic Search",
    "PAID_SEARCH": "Paid Search",
    "EMAIL_MARKETING": "Email Marketing",
    "SOCIAL_MEDIA": "Organic Social",
    "REFERRALS": "Referral",
    "OTHER_CAMPAIGNS": "Other Campaigns",
    "DIRECT_TRAFFIC": "Direct Traffic",
    "OFFLINE": "Offline",
    "PAID_SOCIAL": "Paid Social",
    "AI_REFERRALS": "AI Referrals",
}
UNKNOWN_SOURCE = "Desconhecida"


def _get(session: requests.Session, path: str, params: dict = None) -> dict:
    response = session.get(f"{API}{path}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_stages(session: requests.Session) -> dict:
    """Mapeia id do estágio -> {label, order, closed, won} a partir dos pipelines de deals."""
    stages = {}
    for pipeline in _get(session, "/crm/v3/pipelines/deals")["results"]:
        for stage in pipeline["stages"]:
            meta = stage.get("metadata", {})
            closed = str(meta.get("isClosed", "false")).lower() == "true"
            stages[stage["id"]] = {
                "label": stage["label"],
                "order": stage.get("displayOrder", 0),
                "closed": closed,
                "won": closed and float(meta.get("probability") or 0) >= 1.0,
            }
    return stages


def fetch_deals(session: requests.Session) -> list:
    deals, after = [], None
    while True:
        params = {"limit": 100, "properties": ",".join(DEAL_PROPERTIES), "archived": "false"}
        if after:
            params["after"] = after
        page = _get(session, "/crm/v3/objects/deals", params)
        deals.extend(page["results"])
        after = page.get("paging", {}).get("next", {}).get("after")
        if not after:
            return deals


def _date(value: str) -> str:
    return value[:10] if value else ""


def deal_to_row(deal: dict, stages: dict) -> dict:
    props = deal["properties"]
    stage = stages.get(props.get("dealstage"), {"label": props.get("dealstage") or "", "closed": False, "won": False})
    if stage["closed"]:
        status = "closed_won" if stage["won"] else "closed_lost"
    else:
        status = "open"
    created = _date(props.get("createdate"))
    return {
        "deal_id": deal["id"],
        "deal_name": props.get("dealname") or "",
        "stage": stage["label"],
        "status": status,
        "amount": props.get("amount") or 0,
        "source": SOURCE_LABELS.get(props.get("hs_analytics_source"), UNKNOWN_SOURCE),
        "created_date": created,
        "close_date": _date(props.get("closedate")),
        # Sem atividade registrada, o negócio está parado desde a criação
        "last_activity_date": _date(props.get("notes_last_updated")) or created,
        "contacts_engaged": props.get("num_associated_contacts") or 0,
    }


def stage_order(stages: dict) -> list:
    """Labels dos estágios abertos, na ordem do pipeline (sem duplicatas)."""
    ordered = sorted((s for s in stages.values() if not s["closed"]), key=lambda s: s["order"])
    return list(dict.fromkeys(s["label"] for s in ordered))


def export(out_path: Path, token: str) -> int:
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    stages = fetch_stages(session)
    rows = [deal_to_row(deal, stages) for deal in fetch_deals(session)]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    out_path.with_suffix(".stages.txt").write_text("\n".join(stage_order(stages)), encoding="utf-8")
    return len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/hubspot_pipeline.csv")
    args = parser.parse_args()

    token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("HUBSPOT_ACCESS_TOKEN não definida.")

    count = export(Path(args.out), token)
    print(f"{count} negócios exportados para {args.out}")


if __name__ == "__main__":
    main()
