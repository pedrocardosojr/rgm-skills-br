# Dicionário dos dados

**Vale Alto Alimentos** é uma indústria **fictícia** de bens de consumo, de porte médio, com faturamento a preço de lista de cerca de R$ 95 milhões em 52 semanas (01/12/2025 a 23/11/2026). Todos os números são inventados e gerados por `scripts/gerar_dados.py` (semente fixa, reproduzível). Qualquer semelhança com empresa real é coincidência.

Ela tem 3 categorias, 9 SKUs, 4 canais e 27 eventos promocionais.

| Arquivo | Grão | O que tem |
|---|---|---|
| `produtos.csv` | SKU | Descrição, categoria, tamanho, conteúdo em kg ou L, preço de lista inicial, custo variável unitário e elasticidade-preço |
| `reajustes_lista.csv` | Categoria | Data e percentual do reajuste de lista no período |
| `vendas_semanais.csv` | Semana × SKU × canal | Unidades vendidas, preço de lista vigente, desconto on-invoice, desconto promocional e evento |
| `condicoes_canal.csv` | Canal | Política comercial: on-invoice, rebate, verba de contrato, bonificação, frete, prazo, taxa financeira, markup da revenda e do varejo final, e % da revenda no Simples Nacional |
| `condicoes_especiais.csv` | Canal × SKU | Condições negociadas fora da política, somadas às do canal |
| `promocoes.csv` | Evento | SKU, canal, início, duração, mecânica, desconto e verba fixa paga ao cliente |
| `tributacao_atual.csv` | Categoria | ICMS, PIS/Cofins e IPI no sistema atual (ilustrativo) |
| `tributacao_reforma.csv` | Categoria | Regime na reforma: cesta básica, alíquota padrão e Imposto Seletivo |
| `cronograma_transicao.csv` | Ano (2026-2033) | Alíquotas de CBS e IBS e fatores de PIS/Cofins, IPI e ICMS em cada ano |

## Convenções
- **Preço de lista** (`preco_lista_unit`) inclui ICMS e PIS/Cofins, que são calculados "por dentro". O IPI é cobrado por fora.
- **Ordem dos descontos na nota:** primeiro o on-invoice do canal (mais o especial, se houver), depois o desconto promocional.
- **Off-invoice** (rebate, verba de contrato, bonificação e frete) é um percentual sobre o preço de nota, sem impostos. A verba fixa de promoção vem em R$, por evento.
- **Custo financeiro do prazo** = taxa mensal × prazo em dias ÷ 30, sobre o valor faturado.
- **Distribuidor:** `markup_revenda_pct` é a margem do distribuidor e `markup_varejo_final_pct` é a do pequeno varejo que compra dele.
- **`revenda_no_simples_pct`** é a fatia da revenda no Simples Nacional, que aproveita pouco crédito de CBS/IBS. Isso pesa no repasse da reforma.

## Tributação: leia antes de usar
As alíquotas são **ilustrativas**: não há substituição tributária, benefícios estaduais nem regime monofásico. A CBS (8,8%) e o IBS (17,7%) usam a estimativa de referência de cerca de 26,5% somados. A alíquota oficial ainda estava em discussão em nov/2026, e notícias citavam valores de CBS entre 8,7% e 11,3%. A alíquota do Imposto Seletivo sobre bebidas açucaradas depende de lei ordinária, e os 10% usados aqui são um parâmetro. Base: EC 132/2023 e LC 214/2025, conferidas em 26/11/2026. **Isto não é parecer fiscal.**
