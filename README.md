# Relatório de Pipeline — Análise do Período

## 1. Resumo executivo

Pipeline aberto de R$ 491.000 contra uma meta de R$ 250.000, gerando cobertura de 1,96x — no limite inferior do saudável. O maior risco não está no volume, mas na qualidade: 5 dos 15 negócios abertos (33%) estão estagnados há 18-40 dias, e outros 5 são single-threaded, com sobreposição significativa entre os dois grupos (3 negócios aparecem em ambas as listas). O canal Outbound está arrastando a taxa de conversão geral para baixo (37,5% vs. 75% de Inbound), o que merece atenção antes de escalar investimento nesse canal.

## 2. Métricas-chave

| Métrica | Valor | Leitura |
|---|---|---|
| Win rate geral | 53,3% | Sólido, mas mascara disparidade grande entre fontes |
| Win rate Inbound | 75,0% | Melhor canal, disponível para escalar |
| Win rate Referral | 66,7% | Segundo melhor canal — base amostral provavelmente pequena, verificar N |
| Win rate Outbound | 37,5% | Metade da conversão de Inbound — canal problemático |
| Tamanho médio do negócio | R$ 39.375 | Referência, sem histórico comparativo para julgar tendência |
| Ciclo de vendas médio | 90 dias | Referência; sem baseline anterior para avaliar se está acelerando ou não |
| Velocidade de pipeline | R$ 3.497,81/dia | Métrica composta — útil para acompanhar tendência período a período |
| Cobertura | 1,96x | Apertada frente à meta (ver seção 3) |
| Negócios estagnados | 5 (R$ 191.000, 39% do pipeline) | Risco de atraso ou perda de forecast |
| Negócios single-threaded | 5 (R$ 188.500, 38% do pipeline) | Risco de perda por dependência de um único contato |

**Nota de qualidade de dados:** não há dados de período anterior para comparação de tendência (win rate, ciclo, velocidade). Também não sei o tamanho da amostra por fonte (win rate de 66,7% em Referral pode ser 2 de 3 negócios — instável). Recomendo incluir contagem de negócios por fonte no próximo corte.

## 3. Cobertura

**Apertada.** Regra geral de mercado pede cobertura de 3x a 4x para pipelines com ciclo de 90 dias e win rate ~50%; 1,96x está bem abaixo disso.

O cálculo simplista (491.000 / 250.000 = 1,96x) não pondera por win rate. Se aplicarmos o win rate real de 53,3% como proxy de probabilidade de conversão, o valor esperado do pipeline aberto é de aproximadamente R$ 261.700 — apenas 4,7% acima da meta. Isso significa que **não há margem de segurança**: qualquer perda acima do esperado (por exemplo, se os 5 negócios estagnados — R$ 191.000 — não avançarem) coloca a meta em risco direto.

**Ação recomendada:** aumentar geração de pipeline novo neste período, priorizando Inbound e Referral (win rates mais altos), e não tratar 1,96x como confortável.

## 4. Negócios que precisam de intervenção

### Estagnados
| Negócio | Estágio | Valor | Dias sem atividade | Ação recomendada |
|---|---|---|---|---|
| Nordic Freight Co | Evaluation | R$ 65.000 | 40 | Escalar para call de reengajamento com champion; se sem resposta em 5 dias, marcar como at-risk no forecast |
| Fintra Payments | Proposal | R$ 54.000 | 30 | Confirmar se a proposta ainda está sob avaliação; ligar diretamente para o decisor, não apenas e-mail |
| Lumen Energy Co | Proposal | R$ 29.500 | 25 | Enviar follow-up com prazo claro de decisão; se não houver resposta, requalificar estágio |
| Ironclad Security | Qualification | R$ 24.000 | 22 | Retomar discovery — 22 dias parado em Qualification sugere falta de urgência ou fit não confirmado |
| BrightPath Retail | Proposal | R$ 18.500 | 18 | Follow-up padrão; menor risco relativo, mas monitorar próxima semana |

### Single-threaded
| Negócio | Estágio | Valor | Contatos engajados | Ação recomendada |
|---|---|---|---|---|
| Nordic Freight Co | Evaluation | R$ 65.000 | 1 | **Duplo risco** (também estagnado) — priorizar mapeamento de mais stakeholders antes de qualquer outra ação |
| Fintra Payments | Proposal | R$ 54.000 | 1 | **Duplo risco** — buscar introdução a um segundo contato (financeiro ou usuário final) antes de reenviar proposta |
| Kestrel Biotech | Discovery | R$ 52.000 | 1 | Ainda em estágio inicial — bom momento para mapear org chart antes de avançar |
| Harbor Insurance | Qualification | R$ 38.000 | 1 | Solicitar apresentação a outro stakeholder como condição para avançar para Evaluation |
| Lumen Energy Co | Proposal | R$ 29.500 | 1 | **Duplo risco** — mesma ação de expansão de contatos, combinada com o follow-up de estagnação |

**Destaque de risco composto:** Nordic Freight Co, Fintra Payments e Lumen Energy Co somam R$ 148.500 e estão estagnados **e** single-threaded simultaneamente. Isso é 30% do pipeline aberto concentrado no pior perfil de risco. Recomendo tratamento prioritário nesses três antes de qualquer outro negócio.

## 5. Forecast

Base: pipeline aberto de R$ 491.000, win rate histórico de 53,3% (mas com disparidade forte por fonte), 5 negócios de alto risco totalizando R$ 191.000.

- **Commit — R$ 130.000 a R$ 150.000**
  Considera apenas negócios sem sinal de risco (não estagnados, multi-threaded) em estágios avançados (Proposal/Negotiation), aplicando um win rate conservador de ~65% (próximo ao de Referral/Inbound, fontes mais previsíveis). Exclui os R$ 148.500 de risco composto.

- **Best Case — R$ 190.000 a R$ 210.000**
  Assume que 2 dos 3 negócios de risco composto (estagnados + single-threaded) são reengajados com sucesso nas próximas semanas e avançam, mais conversão normal do restante do pipeline saudável a 53,3%.

- **Upside — R$ 240.000 a R$ 260.000**
  Requer que todos os 5 negócios estagnados sejam reativados **e** convertidos, e que os negócios em Negotiation (R$ 120.000) fechem quase integralmente. Esse cenário depende de intervenção ativa e imediata nos negócios da seção 4 — não é uma extrapolação passiva do histórico.

**Leitura honesta:** mesmo no Best Case, o forecast fica abaixo da meta de R$ 250.000. Atingir a meta neste período depende de ação concreta nos negócios estetup inicial.
