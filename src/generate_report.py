"""
generate_report.py

Fluxo do projeto:
1. Carrega dados de CRM (CSV) — dado real, não inventado.
2. Calcula métricas de pipeline de verdade em Python/pandas (metrics.py).
3. Compara com o snapshot do relatório anterior (history.py).
4. Envia só os números calculados (não o CSV inteiro) pra API do Claude,
   usando o prompt de persona "Pipeline Analyst" como system prompt.
5. Gera os gráficos (charts.py) e salva o relatório em reports/, com data no nome.

Uso:
    export ANTHROPIC_API_KEY="sua-chave-aqui"
    python src/generate_report.py --data data/sample_pipeline.csv --quota 250000

Opcional:
    --as-of AAAA-MM-DD   data de referência (padrão: atividade mais recente do CSV)
    --dry-run            calcula métricas, comparação e gráficos sem chamar o Claude
    ANTHROPIC_MODEL      sobrescreve o modelo usado (padrão: claude-sonnet-5)
"""

import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path

import charts
import history
import metrics

ROOT = Path(__file__).resolve().parent.parent
PERSONA_PATH = ROOT / "agents" / "pipeline_analyst_persona.md"
REPORTS_DIR = ROOT / "reports"
HISTORY_DIR = REPORTS_DIR / "history"
CHARTS_DIR = REPORTS_DIR / "charts"
MODEL = os.environ.get("ANTHROPIC_MODEL") or "claude-sonnet-5"


def load_persona() -> str:
    return PERSONA_PATH.read_text(encoding="utf-8")


def call_claude(persona_prompt: str, metrics_summary: dict) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não definida. Rode: export ANTHROPIC_API_KEY='sua-chave'"
        )

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    user_message = (
        "Aqui estão as métricas de pipeline já calculadas para este período "
        f"(em JSON):\n\n{json.dumps(metrics_summary, indent=2, ensure_ascii=False)}\n\n"
        "Gere o relatório no formato definido nas suas instruções."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=persona_prompt,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": user_message}],
    )

    print(f"stop_reason: {response.stop_reason}")
    print(f"content blocks: {[block.type for block in response.content]}")

    text = "".join(block.text for block in response.content if block.type == "text")

    if response.stop_reason == "max_tokens":
        raise RuntimeError(
            "O relatório foi cortado (stop_reason=max_tokens). Aumente max_tokens."
        )

    if not text.strip():
        raise RuntimeError(
            "A API retornou uma resposta vazia. "
            f"stop_reason={response.stop_reason}, "
            f"blocks={[block.type for block in response.content]}. "
            "Verifique o nome do modelo e os logs acima."
        )

    return text


def load_stage_order(data_path: Path) -> list:
    """Ordem dos estágios gravada pelo exportador do HubSpot, se existir."""
    sidecar = data_path.with_suffix(".stages.txt")
    if sidecar.exists():
        return [line for line in sidecar.read_text(encoding="utf-8").splitlines() if line]
    return None


def charts_section(chart_list: list) -> str:
    lines = ["", "## Gráficos", ""]
    for title, path in chart_list:
        lines += [f"![{title}]({path.relative_to(REPORTS_DIR).as_posix()})", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(ROOT / "data" / "sample_pipeline.csv"))
    parser.add_argument("--quota", type=float, default=150000)
    parser.add_argument(
        "--as-of",
        type=datetime.fromisoformat,
        default=None,
        help="Data de referência AAAA-MM-DD (padrão: atividade mais recente do CSV)",
    )
    parser.add_argument(
        "--single-thread-min",
        type=float,
        default=25000,
        help="Valor mínimo para um negócio com 1 contato ser sinalizado como single-threaded",
    )
    parser.add_argument("--dry-run", action="store_true", help="Não chama o Claude")
    args = parser.parse_args()

    run_date = date.today().isoformat()
    data_path = Path(args.data)
    df = metrics.load_data(data_path)
    metrics_summary = metrics.build_metrics_summary(
        df,
        quota=args.quota,
        as_of=args.as_of,
        stage_order=load_stage_order(data_path),
        single_thread_min_amount=args.single_thread_min,
    )

    past = history.load_history(HISTORY_DIR)
    previous = history.previous_snapshot(past, run_date)
    claude_input = dict(metrics_summary)
    if previous:
        claude_input["comparison_with_previous_report"] = history.compare(
            metrics_summary, previous[1], previous[0]
        )

    print("Métricas calculadas:")
    print(json.dumps(claude_input, indent=2, ensure_ascii=False))

    trend = [(d, s) for d, s in past if d < run_date] + [(run_date, metrics_summary)]
    chart_list = charts.build_charts(metrics_summary, trend, CHARTS_DIR / run_date)

    if args.dry_run:
        print(f"\n--dry-run: {len(chart_list)} gráficos em {CHARTS_DIR / run_date}; Claude não chamado.")
        return

    report_text = call_claude(load_persona(), claude_input)

    REPORTS_DIR.mkdir(exist_ok=True)
    out_path = REPORTS_DIR / f"pipeline_report_{run_date}.md"
    out_path.write_text(report_text.rstrip() + "\n" + charts_section(chart_list), encoding="utf-8")
    # Só grava o snapshot depois do relatório pronto, pra uma falha não poluir o histórico
    history.save_snapshot(HISTORY_DIR, run_date, metrics_summary)

    print(f"\nRelatório salvo em: {out_path}")


if __name__ == "__main__":
    main()
