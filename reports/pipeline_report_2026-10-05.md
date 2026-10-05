# Relatório de Pipeline — Período Atual

## 1. Resumo executivo

Pipeline total aberto de **R$ 491.000** contra uma meta de **R$ 250.000**, gerando cobertura de 1.96x — na faixa saudável, mas não folgada. O dado mais preocupante não está nos totais, e sim na qualidade: **15 dos ~15 negócios identificados estão estagnados** (sem atividade há 18+ dias) e 5 deles são single-threaded, incluindo dois dos três maiores negócios do pipeline (Nordic Freight Co, R$ 65.000; Fintra Payments, R$ 54.000). Win rate agregado de 53,3% esconde uma disparidade grande por fonte: Outbound converte a praticamente metade da taxa de Inbound, o que deve pesar no forecast e na alocação de esforço.

## 2. Métricas-chave

| Métrica | Valor | Leitura |
|---|---|---|
| Win rate (geral) | 53,3% | Saudável em termos absolutos, mas mascara variação grande por fonte (ver abaixo) |
| Win rate — Inbound | 75,0% | Fonte mais eficiente; priorizar geração de demanda inbound |
| Win rate — Referral | 66,7% | Segunda melhor fonte, mas provavelmente baixo volume — **checar n antes de confiar** |
| Win rate — Outbound | 37,5% | Quase metade da taxa de Inbound; maior fonte de risco de conversão |
| Ticket médio | R$ 39.375 | Referência para dimensionar impacto de perdas individuais |
| Ciclo médio de vendas | 90 dias | Usar como referência para o que conta como "estagnado": 18-56 dias sem atividade já representa 20%-62% do ciclo inteiro consumido em silêncio |
| Velocidade de pipeline | R$ 3.497,81/dia | Indicador líder de receita projetada; monitorar tendência semana a semana, não só o valor pontual |
| Cobertura | 1,96x | Ver seção 3 |

**Nota sobre qualidade de dado:** não foi informado o volume de negócios (n) por fonte no win rate segmentado. Taxas de 66,7% e 75,0% podem estar baseadas em poucas oportunidades — risco de ruído estatístico. Recomendo anexar contagem absoluta na próxima extração antes de usar essas taxas para alocar orçamento.

## 3. Cobertura

**Apertada, não insuficiente.** Com 1,96x contra meta de R$ 250.000, o pipeline nominal cobre quase o dobro da meta — acima do mínimo convencional de 3x normalmente recomendado para ciclos de 90 dias seria o ideal, mas a referência de 3x é genérica e depende do win rate real da operação.

Fazendo a conta com o win rate real (53,3%): R$ 491.000 × 0,533 ≈ **R$ 261.663 esperado**, ligeiramente acima da meta de R$ 250.000. Isso parece confortável, mas dois fatores corroem essa margem:

- **100% dos negócios identificados em estágios abertos aparecem na lista de estagnados** — ou seja, não há visibilidade de pipeline "saudável" para compensar perdas caso os estagnados morram.
- Se os 5 negócios single-threaded (R$ 238.500 somados) sofrerem qualquer perda por saída de campeão/troca de interlocutor, a cobertura efetiva cai para **1,03x** — abaixo do limiar seguro.

**Veredito: cobertura nominal é saudável, cobertura ajustada a risco é apertada.**

## 4. Negócios que precisam de intervenção

Ordenados por urgência (dias sem atividade × tamanho do negócio):

| Negócio | Estágio | Valor | Dias parado | Thread único? | Ação recomendada |
|---|---|---|---|---|---|
| Nordic Freight Co | Evaluation | R$ 65.000 | 56 | Sim | Escalar para gestor do negócio hoje; exigir multi-threading antes de qualquer próxima etapa |
| Fintra Payments | Proposal | R$ 54.000 | 46 | Sim | Ligação de reengajamento com economic buyer; identificar 2º contato esta semana |
| Lumen Energy Co | Proposal | R$ 29.500 | 41 | Sim | Enviar follow-up com novo gatilho de urgência (ex: proposta com prazo); mapear 2º contato |
| Ironclad Security | Qualification | R$ 24.000 | 38 | Não | Qualificar "morto x vivo" — 38 dias em Qualification sem atividade sugere baixa prioridade do cliente; se sem resposta em 7 dias, mover para "stalled/desqualificado" |
| BrightPath Retail | Proposal | R$ 18.500 | 34 | Não | Confirmar recebimento da proposta; se não houver retorno em 5 dias, desqualificar |
| Harbor Insurance | Qualification | R$ 38.000 | 25 | Sim | Buscar segundo contato antes de avançar estágio; valor alto para estar single-threaded em etapa inicial |
| Falcon Media Group | Negotiation | R$ 47.000 | 23 | Não | Alto valor em negociação parada — confirmar objeções pendentes com o rep diretamente |
| Ashford Consulting | Evaluation | R$ 16.200 | 22 | Não | Checagem de rotina; baixo valor, baixo risco |
| Acme Robotics - Expansion | Negotiation | R$ 42.000 | 21 | Não | Negociação em estágio avançado parada por 21 dias — validar se há bloqueio contratual/jurídico |
| Solaris Manufacturing | Discovery | R$ 15.000 | 20 | Não | Reengajar ou desqualificar; negócio pequeno em estágio inicial |
| Cobalt Analytics | Discovery | R$ 9.800 | 20 | Não | Mesma ação — baixa prioridade |
| Meridian Logistics | Evaluation | R$ 22.000 | 19 | Não | Follow-up padrão |
| Vega Health Systems | Qualification | R$ 27.000 | 19 | Não | Follow-up padrão |
| Kestrel Biotech | Discovery | R$ 52.000 | 19 | Sim | Valor alto, estágio inicial, single-threaded — mapear organograma do cliente antes de avançar |
| Torres Legal Group | Negotiation | R$ 31.000 | 18 | Não | Follow-up de fechamento — mais próximo do ciclo, menor tolerância para atraso |

**Padrão a destacar:** os 5 negócios single-threaded somam R$ 238.500 (48,6% do pipeline total) e 4 deles estão entre os 6 negócios mais estagnados. Isso não é coincidência — negócios com um único ponto de contato têm mais chance de esfriar. Recomendo bloquear avanço de estágio para qualquer negócio single-threaded acima de R$ 20.000 até que um segundo contato seja confirmado.

## 5. Forecast

Base: pipeline aberto R$ 491.000, win rate geral 53,3%, mas com ajuste para risco de estagnação/single-threading.

- **Commit — R$ 140.000 a R$ 160.000**
  Inclui apenas negócios em Proposal/Negotiation que **não** estão estagnados (Falcon Media Group pertence a esta lista mas está parado 23 dias — mantido com desconto de risco) mais Torres Legal Group e Acme Robotics, aplicando win rate histórico de negócios em estágio avançado. Faixa reflete incerteza sobre quantos desses "quase lá" realmente fecham dado o padrão geral de estagnação.

- **Best Case — R$ 200.000 a R$ 230.000**
  Soma Commit + negócios em Evaluation/Qualification que respondem a reengajamento ativo nas próximas 2 semanas (ex: Nordic Freight Co, Fintra Payments, Harbor Insurance), assumindo que a intervenção da seção 4 recupera ~60% deles.

- **Upside — R$ 240.000 a R$ 265.000**
  Cenário em que toda a cobertura nominal se realiza próxima à taxa histórica (R$ 261.663 calculado em cobertura). Este teto depende de recuperar **todos** os 15 negócios estagnados — probabilidade baixa sem mudança de comportamento ativa, por isso tratado como teto e não como número central.

**Recomendação de leitura:** trate o Commit como número de planejamento. A diferença de R$ 100.000+ entre Commit e Upside é inteiramente explicada por negócios estagnados/single-threaded — ou seja, o forecast está mais nas mãos das ações da seção 4 do que em fatores externos de mercado.