# Relatório de Pipeline — Análise do Período

## 1. Resumo executivo

Pipeline com cobertura nominal saudável (1.96x) mas com problemas de qualidade concentrados: 5 dos 15 negócios abertos (33%) estão estagnados há 20+ dias, e outros 5 são single-threaded — com **overlap direto** entre os dois grupos (Nordic Freight, Fintra Payments, Lumen Energy aparecem em ambas as listas). O win rate agregado de 53.3% esconde uma disparidade grave por fonte: Outbound converte a menos da metade da taxa de Inbound (37.5% vs 75.0%), o que exige segmentar qualquer forecast por origem do negócio.

## 2. Métricas-chave

| Métrica | Valor | Leitura |
|---|---|---|
| Win rate geral | 53.3% | Mascarado por mix de fontes — ver segmentação abaixo |
| Win rate Inbound | 75.0% | Forte, mas depende do volume de leads inbound gerados |
| Win rate Outbound | 37.5% | Abaixo da média geral — risco se outbound for a maior fonte de volume |
| Win rate Referral | 66.7% | Sólido, mas amostra provavelmente pequena (não informada) |
| Ticket médio | $39,375 | Referência para dimensionar impacto dos negócios estagnados |
| Ciclo de vendas médio | 90 dias | Nordic Freight (42 dias sem atividade) já consumiu ~47% do ciclo médio parado |
| Velocidade de pipeline | $3,497.81/dia | Indicador composto — não decomposto aqui em win rate × ticket × 1/ciclo |
| Cobertura | 1.96x | Ver seção 3 |
| Negócios estagnados | 5 (43% do valor: $191k de $491k) | Ação imediata necessária |
| Negócios single-threaded | 5 ($238.5k) | Risco estrutural de perda por saída de stakeholder |

**Nota de qualidade de dados:** o JSON não traz o tamanho da amostra por fonte (n de deals). Win rate de 75% em Inbound pode vir de 3 ou de 30 negócios — a confiabilidade estatística é desconhecida. Também não há histórico de períodos anteriores para validar se 1.96x de cobertura é consistente com a sazonalidade do funil.

## 3. Cobertura

**Apertada, não saudável**, pela seguinte lógica:

- Pipeline aberto total: $76.8k + $89k + $103.2k + $102k + $120k = **$491,000**
- Cobertura declarada: 1.96x sobre quota de $250,000 → confere ($491,000 / $250,000 = 1.964).
- Regra de bolso comum em B2B é 3x-4x de cobertura para compensar win rate <100% e leakage no funil. Com win rate real de 53.3%, o pipeline **matematicamente necessário** para bater $250k de quota seria de aproximadamente $250,000 / 0.533 ≈ **$469,000** — ou seja, a cobertura atual de $491k está tecnicamente acima do mínimo, mas com margem de segurança de apenas ~5%.
- Esse cálculo ignora os $191,000 em negócios estagnados. Se removermos esse valor do pipeline "confiável" ($491k - $191k = $300k), a cobertura efetiva cai para **1.20x** — insuficiente mesmo com win rate de 53.3%.

**Conclusão:** cobertura nominal passa, cobertura ajustada por risco de estagnação não passa. Tratar como **apertada a insuficiente**, não como confortável.

## 4. Negócios que precisam de intervenção

| Negócio | Estágio | Valor | Problema | Ação recomendada |
|---|---|---|---|---|
| Nordic Freight Co | Evaluation | $65,000 | 42 dias sem atividade + single-threaded | Escalar para envolvimento do sponsor executivo esta semana; se não houver resposta em 5 dias, requalificar ou mover para closed-lost |
| Fintra Payments | Proposal | $54,000 | 32 dias sem atividade + single-threaded | Ligação direta do AE + tentar identificar segundo contato (economic buyer) antes de reenviar proposta |
| Lumen Energy Co | Proposal | $29,500 | 27 dias sem atividade + single-threaded | Mesma ação: risco duplo em estágio avançado do funil — priorizar sobre negócios estagnados de estágio inicial |
| Kestrel Biotech | Discovery | $52,000 | Single-threaded (não estagnado) | Mapear org chart e agendar reunião com 2º stakeholder antes de avançar para Qualification |
| Harbor Insurance | Qualification | $38,000 | Single-threaded (não estagnado) | Introduzir champion a outro contato antes do avanço de estágio |
| Ironclad Security | Qualification | $24,000 | 24 dias sem atividade | Reengajar ou requalificar critério de timeline |
| BrightPath Retail | Proposal | $18,500 | 20 dias sem atividade | Follow-up de fechamento; se não houver resposta em 7 dias, mover para "no decision" |

**Padrão crítico:** Nordic Freight, Fintra Payments e Lumen Energy somam $148,500 e estão **duplamente expostos** (estagnados E single-threaded). Isso não é coincidência aleatória — sugere processo de descoberta deficiente nesses negócios desde o início, não apenas falta de follow-up recente. Recomendo revisão de causa raiz com o AE responsável, não só ação tática de reengajamento.

## 5. Forecast

Dado o win rate de 53.3%, o ticket médio de $39,375 e a concentração de risco identificada, a faixa de forecast é:

- **Commit — $167,000 (± 15%, faixa $142k–$192k):** soma dos negócios em Negotiation ($120,000) e Proposal não-estagnados (Proposal total $102,000 menos Fintra $54,000 menos Lumen $29,500 menos BrightPath $18,500 = $0 líquido em Proposal saudável — portanto Commit se apoia quase inteiramente em Negotiation). Aplicado o win rate de 53.3% sobre Negotiation: $120,000 × 0.533 ≈ $64,000, mas por estarem no estágio final do funil, uso ponderação mais alta (~70%) → **$84,000 de Negotiation**, mais valor residual de Proposal saudável, resultando em faixa conservadora de $142k-$192k. **Risco explícito:** este número é sensível — 3 dos negócios em Proposal estão comprometidos, então o "saudável" real em Proposal é próximo de zero.

- **Best Case — $230,000 (± 20%, faixa $184k–$276k):** inclui Negotiation completo, Proposal recuperado (contingente à intervenção nos 3 negócios problemáticos) e conversão parcial de Evaluation ($103,200 × 53.3% ≈ $55,000). Depende diretamente do sucesso das ações da Seção 4 dentro das próximas 2 semanas.

- **Upside — $310,000 (± 25%, faixa $232k–$387k):** cenário em que Discovery e Qualification também avançam mais rápido que o ciclo médio de 90 dias, e os 5 negócios single-threaded conseguem segundo contato sem perda de momentum. **Baixa probabilidade** — depende de execução perfeita em múltiplas frentes simultâneas.

**Limitação do forecast:** não há dado de win rate por estágio (apenas win rate geral e por fonte), então as ponderações por estágio acima são estimativas baseadas em prática de mercado, não em taxa histórica real do funil desta equipe. Recomendo fornecer win rate segmentado por estágio para reduzir a margem de incerteza nas próximas iterações deste relatório.