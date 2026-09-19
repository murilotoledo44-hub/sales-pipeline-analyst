n# Sales Pipeline Analyst

Projeto de portfólio em Revenue Operations: transforma dados brutos de CRM em um relatório de saúde de pipeline e forecast, calculado de verdade em Python e narrado por IA — automatizado para rodar sozinho toda semana.

## Como funciona

```
CSV de CRM  →  Python/pandas (cálculo real)  →  Claude API (narrativa e recomendação)  →  reports/*.md
                                                        ↑
                                        agents/pipeline_analyst_persona.md
                                           (define formato e regras do relatório)
```

Nenhum número no relatório é inventado ou alucinado pela IA: todas as métricas (win rate, tamanho médio de negócio, ciclo de vendas, velocidade de pipeline, cobertura, negócios estagnados) são calculadas em `src/metrics.py` com pandas puro. A IA só recebe os números já prontos e escreve o diagnóstico, a priorização e o forecast no formato definido no prompt de persona.

## Estrutura

- `data/sample_pipeline.csv` — dataset sintético de exemplo (30 negócios, abertos e fechados)
- `src/metrics.py` — todo o cálculo determinístico (sem chamada de IA)
- `src/generate_report.py` — script principal: carrega dado → calcula → chama a API do Claude → salva relatório
- `agents/pipeline_analyst_persona.md` — system prompt que define o papel, as regras e o formato de saída do relatório
- `reports/` — relatórios gerados (versionados a cada execução automática)
- `.github/workflows/weekly_report.yml` — roda o script toda segunda-feira e commita o relatório sozinho

## Rodar localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave-aqui"
python src/generate_report.py --data data/sample_pipeline.csv --quota 250000
```

## Automação

O workflow em `.github/workflows/weekly_report.yml` roda toda segunda-feira às 08h (UTC) e também pode ser disparado manualmente na aba **Actions** do repositório. Para funcionar, é preciso cadastrar a chave da API como secret do repositório:

`Settings → Secrets and variables → Actions → New repository secret → ANTHROPIC_API_KEY`

## Por que esse projeto

Mostra três coisas que um relatório estático não mostra: capacidade de calcular métrica de pipeline de verdade (não só descrever o que ela significa), integração prática com a API do Claude para gerar análise a partir de dado real, e automação de ponta a ponta via CI/CD — sem intervenção manual após o setup inicial.
