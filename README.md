# Sales Pipeline Analyst

Analista de pipeline de vendas automatizado: puxa os negócios do HubSpot (ou de um CSV), calcula métricas reais, compara com a semana anterior e usa o Claude para transformar esses números em um relatório executivo em Markdown com gráficos — toda segunda-feira, via GitHub Actions.

> **Projeto de portfólio — dados fictícios.** Os negócios no HubSpot vêm do dataset público *CRM Sales Opportunities* da [Maven Analytics](https://mavenanalytics.io/data-playground/crm-sales-opportunities) (também disponível no Kaggle): pipeline B2B de uma empresa fictícia de hardware (MavenTech), com 499 oportunidades de out/2016 a dez/2017. Todos os valores estão em **dólares (USD)**.

## Como funciona

```
HubSpot ──► src/hubspot_source.py ──► CSV ──► src/metrics.py ──► JSON de métricas ─┬─► Claude ──► reports/pipeline_report_AAAA-MM-DD.md
                                                     reports/history/ (semana anterior) ─┤
                                                                     src/charts.py ──────┴─► reports/charts/AAAA-MM-DD/*.png
```

1. **`src/hubspot_source.py`** — exporta os negócios do HubSpot via API e converte para o formato de CSV abaixo (estágio, status ganho/perdido, fonte, última atividade, contatos).
2. **`src/metrics.py`** — cálculos determinísticos em pandas (nenhuma IA aqui): win rate geral e por fonte (com tamanho da amostra), ticket médio, ciclo de vendas, velocidade de pipeline, pipeline aberto por estágio, cobertura sobre a meta, negócios estagnados e single-threaded, e qualidade dos dados.
3. **`src/history.py`** — salva um snapshot das métricas em `reports/history/` a cada relatório e calcula a variação contra o anterior (incluindo negócios que entraram ou saíram da lista de estagnados).
4. **`src/charts.py`** — gera os gráficos: pipeline por estágio, win rate por fonte e, a partir do 2º relatório, a evolução do pipeline e da cobertura.
5. **`src/generate_report.py`** — envia **só as métricas calculadas e a comparação** (não o CSV) para a API do Claude, usando `agents/pipeline_analyst_persona.md` como system prompt, e salva o relatório com os gráficos em `reports/`.
6. **`.github/workflows/main.yml`** — roda os testes, exporta do HubSpot, gera o relatório toda segunda às 08:00 UTC e faz commit em `reports/`.

## Rodando localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"
python src/generate_report.py --data data/sample_pipeline.csv --quota 150000

# Com os dados do HubSpot
export HUBSPOT_ACCESS_TOKEN="pat-..."
python src/hubspot_source.py --out data/hubspot_pipeline.csv
python src/generate_report.py --data data/hubspot_pipeline.csv --quota 150000

# Só métricas, comparação e gráficos, sem chamar o Claude
python src/generate_report.py --dry-run
```

| Opção | Padrão | Descrição |
|---|---|---|
| `--data` | `data/sample_pipeline.csv` | CSV exportado do CRM |
| `--quota` | `150000` | Meta do período em USD, usada na cobertura |
| `--as-of` | atividade mais recente do CSV | Data de referência para contar dias sem atividade |
| `--single-thread-min` | `25000` | Valor mínimo (USD) para sinalizar negócio com 1 contato |
| `--dry-run` | — | Não chama o Claude nem grava histórico |
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

Regras: estagnado = 14+ dias sem atividade; single-threaded = 1 contato e valor ≥ `--single-thread-min`.

## Configuração no GitHub

Em **Settings → Secrets and variables → Actions**:

| Tipo | Nome | Para quê |
|---|---|---|
| Secret | `ANTHROPIC_API_KEY` | Obrigatório — gera o texto do relatório |
| Secret | `HUBSPOT_ACCESS_TOKEN` | Puxa os negócios do HubSpot. Sem ele, o workflow usa `data/sample_pipeline.csv` |
| Variable | `PIPELINE_QUOTA` | Meta do período em USD (padrão `150000`) |
| Variable | `SINGLE_THREAD_MIN` | Valor mínimo para single-threaded (padrão `25000`) |
| Variable | `ANTHROPIC_MODEL` | Opcional — troca o modelo |

**Token do HubSpot:** em HubSpot → *Settings → Integrations → Private Apps → Create a private app*, marque o escopo `crm.objects.deals.read` e copie o token de acesso.

Para rodar na hora: aba **Actions → Weekly Pipeline Report → Run workflow**.

**Por que a meta padrão é $150,000?** É a média trimestral de receita ganha nos três trimestres completos do dataset (Q2–Q4 2017: $188.5k, $157.7k e $125.8k ≈ $157k), arredondada para baixo. Contra o pipeline aberto atual (~$264k em 117 negócios), isso dá uma cobertura de ~1.8x.

> O CSV exportado do HubSpot não é commitado (está no `.gitignore`); os relatórios em `reports/` citam nomes e valores dos negócios fictícios do dataset. Se um dia usar dados reais de clientes, torne o repositório privado.

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
src/hubspot_source.py                # exportação do HubSpot
src/metrics.py                       # cálculos de pipeline
src/history.py                       # snapshots e comparação semana a semana
src/charts.py                        # gráficos PNG
src/generate_report.py               # orquestra tudo + Claude
tests/                               # testes
reports/                             # relatórios gerados
reports/history/                     # snapshots de métricas (JSON)
reports/charts/                      # gráficos de cada relatório
```
