# Sales Pipeline Analyst

Analista de pipeline de vendas automatizado: calcula métricas reais a partir de um CSV de CRM e usa o Claude para transformar esses números em um relatório executivo em Markdown — toda segunda-feira, via GitHub Actions.

## Como funciona

```
data/*.csv ──► src/metrics.py ──► JSON de métricas ──► Claude (persona Pipeline Analyst) ──► reports/pipeline_report_AAAA-MM-DD.md
```

1. **`src/metrics.py`** — cálculos determinísticos em pandas (nenhuma IA aqui): win rate geral e por fonte (com tamanho da amostra), ticket médio, ciclo de vendas, velocidade de pipeline, pipeline aberto por estágio, cobertura sobre a meta, negócios estagnados e single-threaded.
2. **`src/generate_report.py`** — envia **só as métricas calculadas** (não o CSV) para a API do Claude, usando `agents/pipeline_analyst_persona.md` como system prompt, e salva o relatório em `reports/`.
3. **`.github/workflows/main.yml`** — roda os testes, gera o relatório toda segunda às 08:00 UTC e faz commit em `reports/`.

## Rodando localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"
python src/generate_report.py --data data/sample_pipeline.csv --quota 250000
```

| Opção | Padrão | Descrição |
|---|---|---|
| `--data` | `data/sample_pipeline.csv` | CSV exportado do CRM |
| `--quota` | `250000` | Meta do período, usada na cobertura |
| `--as-of` | atividade mais recente do CSV | Data de referência para contar dias sem atividade |
| `ANTHROPIC_MODEL` (env) | `claude-sonnet-5` | Modelo do Claude usado no relatório |

> **Por que `--as-of`?** Os dias sem atividade são contados a partir da data do extrato, não de hoje. Assim, um CSV estático não "envelhece" sozinho e marca todo o pipeline como estagnado.

## Formato do CSV

| Coluna | Exemplo | Observação |
|---|---|---|
| `deal_id` | `1001` | |
| `deal_name` | `Acme Robotics - Expansion` | |
| `stage` | `Negotiation` | Discovery, Qualification, Evaluation, Proposal, Negotiation, Won, Lost |
| `status` | `open` | `open`, `closed_won` ou `closed_lost` |
| `amount` | `42000` | |
| `source` | `Outbound` | Inbound, Outbound, Referral… |
| `created_date`, `close_date`, `last_activity_date` | `2026-06-02` | ISO (AAAA-MM-DD) |
| `contacts_engaged` | `3` | Contatos envolvidos no negócio |

Regras: estagnado = 14+ dias sem atividade; single-threaded = 1 contato e valor ≥ R$ 25.000.

## Configuração no GitHub

1. Em **Settings → Secrets and variables → Actions**, crie o secret `ANTHROPIC_API_KEY`.
2. Para usar seus dados, substitua `data/sample_pipeline.csv` (ou altere `--data` no workflow).
3. Para rodar na hora: aba **Actions → Weekly Pipeline Report → Run workflow**.

## Testes

```bash
pip install pytest
pytest -q
```

Os testes também rodam a cada push/PR (`.github/workflows/tests.yml`).

## Estrutura

```
agents/pipeline_analyst_persona.md   # system prompt do analista
data/sample_pipeline.csv             # dados de exemplo
src/metrics.py                       # cálculos de pipeline
src/generate_report.py               # orquestra métricas + Claude
tests/test_metrics.py                # testes dos cálculos
reports/                             # relatórios gerados
```
