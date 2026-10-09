"""Testes do mapeamento HubSpot -> CSV (sem chamar a API)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import hubspot_source  # noqa: E402

STAGES = {
    "1": {"label": "Prospecting", "order": 0, "closed": False, "won": False},
    "2": {"label": "Negotiation", "order": 4, "closed": False, "won": False},
    "3": {"label": "Closed Won", "order": 5, "closed": True, "won": True},
    "4": {"label": "Closed Lost", "order": 6, "closed": True, "won": False},
}


def deal(stage, **props):
    base = {"dealname": "Acme", "dealstage": stage, "createdate": "2026-09-01T12:00:00Z"}
    base.update(props)
    return {"id": "42", "properties": base}


def test_open_deal_mapping():
    row = hubspot_source.deal_to_row(
        deal("2", amount="1500.5", hs_analytics_source="REFERRALS",
             notes_last_updated="2026-09-20T10:00:00Z", num_associated_contacts="2"),
        STAGES,
    )
    assert row["stage"] == "Negotiation"
    assert row["status"] == "open"
    assert row["amount"] == "1500.5"
    assert row["source"] == "Referral"
    assert row["created_date"] == "2026-09-01"
    assert row["last_activity_date"] == "2026-09-20"
    assert row["contacts_engaged"] == "2"


def test_closed_status():
    assert hubspot_source.deal_to_row(deal("3"), STAGES)["status"] == "closed_won"
    assert hubspot_source.deal_to_row(deal("4"), STAGES)["status"] == "closed_lost"


def test_missing_fields_fall_back():
    row = hubspot_source.deal_to_row(deal("1"), STAGES)
    assert row["amount"] == 0
    assert row["source"] == hubspot_source.UNKNOWN_SOURCE
    # Sem atividade registrada, conta desde a criação
    assert row["last_activity_date"] == "2026-09-01"
    assert row["contacts_engaged"] == 0


def test_stage_order_only_open_stages():
    assert hubspot_source.stage_order(STAGES) == ["Prospecting", "Negotiation"]
