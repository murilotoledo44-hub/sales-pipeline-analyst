# Relatório de Pipeline — Diagnóstico do Período

## 1. Resumo executivo

O pipeline tem cobertura nominal saudável (1.96x) e win rate agregado de 53.3%, mas esses números escondem dois problemas estruturais: **15 dos 15 negócios totais em aberto estão estagnados** (≥25 dias sem atividade) e o canal Outbound está performando a quase metade do Inbound em win rate (37.5% vs 75.0%). Isso é um pipeline que parece saudável no agregado mas está operacionalmente parado — a cobertura de 1.96x é um número do passado (criação de pipeline), não uma garantia de fechamento.

## 2. Métricas-chave

| Métrica | Valor | Leitura |
|---|---|---|
| Win rate geral | 53.3% | Saudável no agregado, mas mascara disparidade por fonte (ver seção 3/cobertura) |
| Win rate — Inbound | 75.0% | Melhor fonte, de longe |
| Win rate — Referral | 66.7% | Segunda melhor, mas atenção ao volume (base amostral não informada) |
| Win rate — Outbound | 37.5% | Quase metade do Inbound — risco de qualificação na entrada |
| Avg deal size | $39,375 | Referência única; sem segmentação por fonte/estágio no JSON para validar consistência |
| Ciclo de vendas médio | 90 dias | Referência para calcular estagnação — ver seção 4 |
| Velocity | $3,497.81/dia | Leading indicator de saúde de receita; monitorar tendência, não só valor pontual |
| Coverage ratio | 1.96x | Ver análise na seção 3 |
| Negócios estagnados | 15 de 15 (100% do pipeline aberto) | **Crítico** — nenhum negócio aberto teve atividade recente |
| Negócios single-threaded | 5 | Risco de perda silenciosa por falta de redundância de contato |

**Nota de qualidade de dado:** o JSON não traz o número total de negócios "ganhos/perdidos" por fonte em valor absoluto — os win rates por fonte podem estar sobre bases amostrais pequenas e desiguais. Recomendo validar o N antes de usar esses percentuais para realocar budget de SDR/AE.

## 3. Cobertura

**Apertada, não saudável — apesar do número.**

- Regra de bolso de mercado costuma pedir 3x–4x de cobertura para pipelines com win rate ~50% e ciclo de 90 dias. Com 1.96x, a cobertura está **abaixo do recomendado** mesmo considerando o win rate relativamente bom.
- Isso é agravado pelo fato de **100% dos negócios abertos (15/15) estarem estagnados**. Cobertura nominal de 1.96x assume que os negócios no funil estão avançando ativamente — aqui não estão. Na prática, a cobertura "efetiva" (ajustada por negócios vivos) é mais próxima de zero até que esses negócios sejam reengajados ou desqualificados.
- Diagnóstico: a cobertura reportada reflete pipeline **criado**, não pipeline **em movimento**. É um indicador atrasado dando falsa segurança.

## 4. Negócios que precisam de intervenção

### Estagnados (ordenados por dias sem atividade — todos os 15 do pipeline aberto)

| Negócio | Estágio | Valor | Dias parado | Ação recomendada |
|---|---|---|---|---|
| Nordic Freight Co | Evaluation | $65,000 | 63 | Contato executivo direto hoje; se sem resposta em 5 dias, mover para "at risk" e reduzir peso no forecast |
| Fintra Payments | Proposal | $54,000 | 53 | Reconfirmar proposta com decisor; verificar se concorrente entrou no ciclo |
| Lumen Energy Co | Proposal | $29,500 | 48 | Ligação de desbloqueio + oferta de call técnica para reengajar |
| Ironclad Security | Qualification | $24,000 | 45 | Requalificar ou desqualificar — 45 dias parado em Qualification é sinal de fit fraco |
| BrightPath Retail | Proposal | $18,500 | 41 | Confirmar orçamento aprovado; se não, degradar estágio |
| Harbor Insurance | Qualification | $38,000 | 32 | Multithread imediatamente (ver lista abaixo) + agendar discovery call |
| Falcon Media Group | Negotiation | $47,000 | 30 | Negociação parada é crítico — escalar para gestor de conta, prazo de resposta em 48h |
| Ashford Consulting | Evaluation | $16,200 | 29 | Enviar case study + agendar follow-up estruturado |
| Acme Robotics - Expansion | Negotiation | $42,000 | 28 | Confirmar status de contrato/legal; risco de perder momentum de expansão |
| Solaris Manufacturing | Discovery | $15,000 | 27 | Reengajar ou desqualificar — 27 dias parado em Discovery é sinal fraco |
| Cobalt Analytics | Discovery | $9,800 | 27 | Mesmo tratamento — avaliar fit antes de investir mais tempo |
| Meridian Logistics | Evaluation | $22,000 | 26 | Follow-up com nova oferta de valor (ROI calc, benchmark) |
| Vega Health Systems | Qualification | $27,000 | 26 | Confirmar critérios de compra; recolocar na cadência |
| Kestrel Biotech | Discovery | $52,000 | 26 | Prioridade alta (ticket grande) — multithread + follow-up executivo |
| Torres Legal Group | Negotiation | $31,000 | 25 | Fechar loop de negociação esta semana; risco de esfriar |

**Leitura agregada:** negócios em Negotiation (Falcon, Acme, Torres — $120,000 total) estagnados por 25–30 dias são a prioridade número um: são os mais próximos de fechar e os que mais pesam no forecast de curto prazo.

### Single-threaded (risco de contato único — 5 negócios, $238,500 em exposição)

| Negócio | Estágio | Valor | Ação recomendada |
|---|---|---|---|
| Nordic Freight Co | Evaluation | $65,000 | Mapear org chart e envolver segundo stakeholder (técnico ou financeiro) antes da próxima reunião |
| Fintra Payments | Proposal | $54,000 | Envolver champion econômico antes do fechamento — risco alto por estar em Proposal com 1 contato |
| Kestrel Biotech | Discovery | $52,000 | Identificar segundo contato já na fase de discovery, dado o ticket alto |
| Harbor Insurance | Qualification | $38,000 | Combinar com ação de estagnação acima — multithread na próxima interação |
| Lumen Energy Co | Proposal | $29,500 | Buscar contato adicional antes de seguir para Negotiation |

**Atenção:** Nordic Freight Co, Fintra Payments, Harbor Insurance e Lumen Energy Co aparecem **simultaneamente** em estagnado e single-threaded — são os 4 negócios de maior risco combinado no pipeline, totalizando $186,500.

## 5. Forecast

Dado que 100% do pipeline aberto está estagnado, o forecast abaixo pondera fortemente esse risco em vez de usar apenas coverage ratio e win rate histórico.

- **Commit — $120,000** (razão: valor total em Negotiation; mesmo estagnados, são os negócios mais avançados no funil e com maior probabilidade de fechar neste ciclo, ajustado para baixo pelo histórico de 30 dias de inatividade em todos os três)
- **Best Case — $222,000** (razão: Negotiation + Proposal, $120,000 + $102,000, assumindo reengajamento bem-sucedido de pelo menos parte dos negócios em Proposal nas próximas 2 semanas)
- **Upside — $330,000 a $391,200** (razão: total do pipeline aberto excluindo/incluindo Discovery; limite superior é teórico e improvável dado que 100% dos negócios estão parados — tratar como teto especulativo, não meta realista)

**Faixa recomendada para planejamento: $120,000–$222,000**, com confiança moderada-baixa. A amplitude é larga de propósito: a estagnação generalizada do pipeline introduz incerteza real sobre quantos desses negócios ainda estão vivos. Recomendo revalidar esse forecast em 7 dias após as ações de reengajamento da seção 4 — sem esse reengajamento, o número realista tende para a ponta inferior do Commit.