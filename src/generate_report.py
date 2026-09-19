"""
generate_report.py

Fluxo do projeto:
1. Carrega dados de CRM (CSV) — dado real, não inventado.
2. Calcula métricas de pipeline de verdade em Python/pandas (metrics.py).
3. Envia só os números calculados (não o CSV inteiro) pra API do Claude,
   usando o prompt de persona "Pipeline Analyst" como system prompt.
4. Salva o relatório gerado em reports/, com data no nome do arquivo.

Uso:
    export ANTHROPIC_API_KEY="sua-chave-aqui"
    python src/generate_report.py --data data/sample_pipeline.csv --quota 250000
"""

import argparse
import json
import os
from datetime import date
from pathlib import Path

import anthropic

import metrics

ROOT = Path(__file__).resolve().parent.parent
PERSONA_PATH = ROOT / "agents" / "pipeline_analyst_persona.md"
REPORTS_DIR = ROOT / "reports"
MODEL = "claude-sonnet-5"  # ajuste conforme o modelo disponível na sua conta/API


def load_persona() -> str:
    return PERSONA_PATH.read_text(encoding="utf-8")


def call_claude(persona_prompt: str, metrics_summary: dict) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não definida. Rode: export ANTHROPIC_API_KEY='sua-chave'"
        )

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
        messages=[{"role": "user", "content": user_message}],
    )

    print(f"stop_reason: {response.stop_reason}")
    print(f"content blocks: {[block.type for block in response.content]}")

    text = "".join(block.text for block in response.content if block.type == "text")

    if not text.strip():
        raise RuntimeError(
            "A API retornou uma resposta vazia. "
            f"stop_reason={response.stop_reason}, "
            f"blocks={[block.type for block in response.content]}. "
            "Verifique o nome do modelo e os logs acima."
        )

    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(ROOT / "data" / "sample_pipeline.csv"))
    parser.add_argument("--quota", type=float, default=250000)
    args = parser.parse_args()

    df = metrics.load_data(args.data)
    metrics_summary = metrics.build_metrics_summary(df, quota=args.quota)

    print("Métricas calculadas:")
    print(json.dumps(metrics_summary, indent=2, ensure_ascii=False))

    persona_prompt = load_persona()
    report_text = call_claude(persona_prompt, metrics_summary)

    REPORTS_DIR.mkdir(exist_ok=True)
    out_path = REPORTS_DIR / f"pipeline_report_{date.today().isoformat()}.md"
    out_path.write_text(report_text, encoding="utf-8")

    print(f"\nRelatório salvo em: {out_path}")


if __name__ == "__main__":
    main()
