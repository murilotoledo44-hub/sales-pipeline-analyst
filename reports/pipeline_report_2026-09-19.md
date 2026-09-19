# Relatório de Pipeline

## 1. Resumo executivo

O pipeline tem cobertura numérica adequada (1.96x) e win rate agregado saudável (53.3%), mas isso mascara um problema sério de concentração de risco: **5 dos 15 negócios em aberto estão estagnados e 5 estão single-threaded**, com sobreposição significativa entre os dois grupos. O maior risco não é volume — é qualidade de execução em negócios de estágio avançado (Proposal, Evaluation), que é onde estagnação custa mais caro.

## 2. Métricas-chave

| Métrica | Valor | Leitura |
|---|---|---|
| Win rate geral | 53.3% | Sólido, mas varia fortemente por fonte (ver abaixo) |
| Win rate — Inbound | 75.0% | Melhor fonte, priorizar alocação de esforço aqui |
| Win rate — Referral | 66.7% | Forte, mas provavelmente volume baixo — checar N |
| Win rate — Outbound | 37.5% | Quase metade do inbound; investigar qualificação ou SDR targeting |
| Deal size médio | $39,375 | Referência para dimensionar forecast |
| Ciclo de vendas médio | 90 dias | Usar como baseline para julgar estagnação (ver seção 4) |
| Velocity | $3,497.81/dia | Indicador de saúde geral do motor de receita |
| Cobertura | 1.96x | Abaixo do benchmark comum de 3x — ver seção 3 |
| Negócios estagnados | 5 de 15 (33%) | Alto — leading indicator de risco de forecast |
| Negócios single-threaded | 5 de 15 (33%) | Alto — risco de perda por falta de múltiplos stakeholders |

**Nota de qualidade de dados:** o win rate por fonte não vem acompanhado de contagem de negócios (N). Um win rate de 66.7% em Referral pode representar 2 de 3 negócios — amostra pequena demais para tratar como tendência confiável. Recomendo reportar N junto com win rate por fonte nos próximos cortes.

## 3. Cobertura

**Insuficiente**, não saudável.

- Pipeline aberto total: $76,800 + $89,000 + $103,200 + $102,000 + $120,000 = **$491,000**
- Quota: $250,000
- Cobertura: 1.96x

O benchmark de mercado para cobertura saudável fica geralmente entre 3x–4x, considerando que nem todo pipeline fecha. Com win rate de 53.3%, o pipeline atual sozinho geraria uma expectativa matemática de ~$261,753 (53.3% de $491,000) — tecnicamente acima da quota, mas isso assume que **todos** os negócios progridem, o que contradiz diretamente os dados de estagnação e single-threading abaixo. Na prática, a cobertura efetiva (descontando negócios em risco) é mais estreita do que o número bruto sugere.

**Ação recomendada:** aumentar geração de pipeline novo em Discovery/Qualification nas próximas 2-3 semanas — esses estágios têm menor valor total ($76,800 e $89,000) e são os que sustentam cobertura futura.

## 4. Negócios que precisam de intervenção

Dois negócios aparecem em **ambas** as listas — estagnados e single-threaded — e são prioridade máxima.

| Negócio | Estágio | Valor | Problema | Ação recomendada |
|---|---|---|---|---|
| **Nordic Freight Co** | Evaluation | $65,000 | 40 dias sem atividade + único contato | Maior risco do pipeline. Escalar para envolvimento executivo (seu VP com o deles) esta semana. Se não houver resposta em 5 dias úteis, mover para "at risk" no forecast. |
| **Fintra Payments** | Proposal | $54,000 | 30 dias sem atividade + único contato | Está em Proposal há tempo suficiente para superar o ciclo médio (90 dias) sem fechar. Confirmar se a proposta ainda é prioridade do comprador; se não houver retorno em 1 semana, requalificar ou desqualificar. |
| **Lumen Energy Co** | Proposal | $29,500 | 25 dias sem atividade + único contato | Mesma lógica do Fintra. Buscar segundo contato antes de reengajar — enviar proposta sozinho de novo não resolve o risco estrutural. |
| **Ironclad Security** | Qualification | $24,000 | 22 dias sem atividade | Estágio inicial parado — sinal de baixa prioridade do comprador. Fazer uma tentativa de reengajamento direta; se sem resposta em 10 dias, desqualificar para limpar o forecast. |
| **BrightPath Retail** | Proposal | $18,500 | 18 dias sem atividade | Mais recente entre os estagnados, ainda recuperável. Follow-up esta semana. |
| **Harbor Insurance** | Qualification | $38,000 | Single-threaded (não estagnado) | Ainda ativo, mas risco estrutural. Mapear organograma do comprador e identificar segundo stakeholder antes de avançar para Evaluation. |
| **Kestrel Biotech** | Discovery | $52,000 | Single-threaded (não estagnado) | Estágio inicial — momento certo para insistir em multi-threading antes de investir mais tempo de proposta. |

**Padrão a observar:** 3 dos 4 negócios em Proposal/Evaluation têm exatamente esse perfil de risco duplo. Isso não é coincidência — sugere que o processo de qualificação não está forçando multi-threading antes de avançar de estágio. Recomendo revisar critérios de saída de Qualification para exigir 2+ contatos engajados.

## 5. Forecast

Base: pipeline aberto $491,000, win rate 53.3%, quota $250,000.

| Cenário | Valor | Raciocínio |
|---|---|---|
| **Commit** | **$180,000 – $210,000** | Exclui os 5 negócios estagnados ($191,000 em risco direto) do cálculo de probabilidade plena. Aplica win rate ponderado apenas aos negócios com atividade recente e engajamento saudável. |
| **Best Case** | **$230,000 – $260,000** | Assume que Fintra ($54,000) e BrightPath ($18,500) — os estagnados mais recentes/recuperáveis — reengajam e fecham dentro do padrão de 53.3%. Nordic Freight fica de fora por ser o de maior risco. |
| **Upside** | **$280,000 – $310,000** | Assume recuperação de todos os 5 estagnados via intervenção ativa e conversão dos single-threaded (Harbor, Kestrel) acima da média por já estarem em estágios iniciais com tempo de reação. Requer execução das ações da seção 4 nos próximos 10 dias — não é um cenário passivo. |

**Por que não dou um único número:** a diferença entre Commit e Upside é de ~$100,000-130,000, quase metade da quota. Essa variância vem diretamente da incerteza sobre os 5 negócios estagnados — não é ruído estatístico, é risco identificável e acionável. Tratar isso como um ponto único de forecast escondería exatamente o risco que essa análise existe para expor.

**Recomendação de acompanhamento:** reavaliar em 7 dias após as ações de reengajamento da seção 4. Se Nordic Freight e Fintra continuarem sem atividade após contato direto, mover Commit para o piso ($180,000) com alta confiança.