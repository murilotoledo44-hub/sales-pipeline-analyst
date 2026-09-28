# Relatório de Pipeline — Período Atual

## 1. Resumo executivo

O pipeline tem cobertura nominal saudável (1.96x) e win rate agregado de 53.3%, mas isso esconde um problema sério: 9 dos 15 negócios abertos (60%) estão estagnados há 14–49 dias, e 5 negócios somando US$ 238.700 dependem de um único contato. O Outbound está performando muito abaixo do Inbound e Referral, e a maior parte do pipeline em estágios avançados (Proposal, Negotiation) está justamente onde a estagnação é mais concentrada — isso é um risco de forecast, não só de higiene de CRM.

## 2. Métricas-chave

| Métrica | Valor | Leitura |
|---|---|---|
| Win rate geral | 53.3% | Saudável em nível agregado, mas mascara variação grande por fonte (ver abaixo) |
| Win rate — Inbound | 75.0% | Melhor canal, disparado |
| Win rate — Referral | 66.7% | Segundo melhor canal |
| Win rate — Outbound | 37.5% | Quase metade do Inbound — investigar qualificação ou ICP do outbound |
| Deal size médio | US$ 39.375 | Referência única; sem segmentação por fonte/segmento, uso limitado |
| Ciclo de vendas médio | 90 dias | Referência-base; comparar com dados de estagnação abaixo |
| Velocity do pipeline | US$ 3.497,81/dia | Indicador composto; só é útil se comparado a períodos anteriores (dado não disponível aqui) |
| Cobertura | 1,96x | Ver seção 3 |

**Nota de qualidade de dado:** não há série histórica para win rate, velocity ou ciclo de vendas — não é possível dizer se essas métricas estão melhorando, piorando ou estáveis. Toda leitura aqui é de nível absoluto, não de tendência.

## 3. Cobertura

Cobertura de **1.96x** contra meta de US$ 250.000 (pipeline aberto total: US$ 491.000).

Regra geral de mercado considera 3x-4x como faixa saudável para um ciclo de 90 dias com win rate de ~53%. Em **1.96x**, a cobertura está **apertada**, não saudável — mesmo que o win rate atual (53.3%) seja bom, a matemática não fecha com folga: aplicando 53.3% sobre US$ 491.000 aberto, o valor esperado é ~US$ 261.700, que mal cobre a meta. Qualquer erosão no win rate (por exemplo, se o mix migrar mais para Outbound, cujo win rate é 37.5%) coloca a meta em risco.

**Ação recomendada:** aumentar geração de pipeline novo neste período, priorizando fontes Inbound/Referral, dado o gap de conversão do Outbound.

## 4. Negócios que precisam de intervenção

### Estagnados (9 negócios, US$ 334.200 em risco)

| Negócio | Estágio | Valor | Dias sem atividade | Ação recomendada |
|---|---|---|---|---|
| Nordic Freight Co | Evaluation | US$ 65.000 | 49 | Contato direto do AE + escalar para gestor; risco alto de deal morto — definir critério go/no-go |
| Fintra Payments | Proposal | US$ 54.000 | 39 | Reengajar com nova proposta ou marcar como "closed lost" se não houver resposta em 7 dias |
| Lumen Energy Co | Proposal | US$ 29.500 | 34 | Ligação de check-in; validar se orçamento ainda existe |
| Ironclad Security | Qualification | US$ 24.000 | 31 | Requalificar ou desqualificar — 31 dias parado em Qualification é sinal de baixo fit |
| Harbor Insurance | Qualification | US$ 38.000 | 18 | Follow-up imediato; também é single-threaded (ver abaixo) |
| Falcon Media Group | Negotiation | US$ 47.000 | 16 | Prioridade alta — negócio em Negotiation parado é risco de forecast do trimestre; escalar |
| BrightPath Retail | Proposal | US$ 18.500 | 27 | Reengajar ou desqualificar |
| Ashford Consulting | Evaluation | US$ 16.200 | 15 | Follow-up padrão |
| Acme Robotics - Expansion | Negotiation | US$ 42.000 | 14 | Monitorar de perto — está em estágio final, não deixar passar de 21 dias sem contato |

**Destaque de risco:** Falcon Media Group e Acme Robotics - Expansion estão em **Negotiation** (estágio final) e já mostram sinais de estagnação. Isso é o maior risco imediato ao forecast do trimestre — negócios em Negotiation devem ter cadência de contato mais curta, não mais longa.

### Single-threaded (5 negócios, US$ 238.700 em risco)

| Negócio | Estágio | Valor | Ação recomendada |
|---|---|---|---|
| Nordic Freight Co | Evaluation | US$ 65.000 | Mapear org chart e identificar champion adicional antes de avançar estágio |
| Fintra Payments | Proposal | US$ 54.000 | Envolver economic buyer antes de negociar preço |
| Harbor Insurance | Qualification | US$ 38.000 | Identificar segundo contato ainda em Qualification, antes de investir mais tempo |
| Lumen Energy Co | Proposal | US$ 29.500 | Trazer stakeholder técnico para validar proposta |
| Kestrel Biotech | Discovery | US$ 52.000 | Mapear múltiplos contatos logo no início — ainda há tempo no ciclo |

**Sobreposição de risco:** Nordic Freight Co, Fintra Payments e Lumen Energy Co aparecem em **ambas** as listas — estagnados E single-threaded. Esses três (US$ 148.500 combinados) são os candidatos de maior risco de perda no pipeline atual.

## 5. Forecast

Dado win rate agregado de 53.3%, cobertura apertada de 1.96x, e 60% do pipeline aberto estagnado, o forecast deve refletir essa fragilidade, não o otimismo do win rate isolado.

- **Commit — US$ 120.000–140.000**
  Baseado nos negócios em Negotiation (US$ 120.000 total) descontando risco de estagnação em 2 dos 3 negócios desse estágio. Assume que Falcon Media Group e Acme Robotics recebem intervenção imediata e fecham; sem essa intervenção, o Commit cai para ~US$ 47.000 (só Acme, o menos estagnado).

- **Best Case — US$ 190.000–210.000**
  Inclui Negotiation completo + parte de Proposal (US$ 102.000), aplicando o win rate de 53.3% de forma seletiva — priorizando negócios com múltiplos contatos (excluindo Fintra e Lumen, que são single-threaded e estagnados).

- **Upside — US$ 260.000–280.000**
  Requer resgate bem-sucedido dos 3 negócios de risco duplo (US$ 148.500) mais avanço normal de Discovery/Qualification. Este cenário depende de ação corretiva nos próximos 7–10 dias — não é uma extrapolação passiva do pipeline atual.

**Limitação explícita:** não há dados históricos de conversão por estágio nem taxa de "slippage" de período anterior. Essas faixas são construídas a partir do estado atual do pipeline e do win rate agregado, não de um modelo de conversão por estágio calibrado — trate como estimativa de primeira ordem, não como forecast estatístico.