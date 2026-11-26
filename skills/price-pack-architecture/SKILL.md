---
name: price-pack-architecture
description: Analisa a price-pack architecture (PPA) de bens de consumo, ou seja, a escada de preço por tamanho e embalagem. Calcula o preço por kg ou litro na prateleira, os degraus entre tamanhos, a participação em volume e a margem de bolso por kg ou litro, e encontra inversões, degraus fracos, lacunas e dependência de um tamanho de margem baixa. Simula o efeito de lançar, repreçar ou tirar um tamanho, com a origem do volume e cenários. Use quando pedirem "PPA", "price-pack architecture", "escada de preço", "preço por kg", "lacuna de portfólio", "lançar um tamanho novo", "multipack", "downsizing" ou "price point".
---

# Price-pack architecture

A escada de tamanhos decide quanto o shopper paga por kg ou litro e para onde o volume vai quando o preço muda. A pergunta é: **a escada orienta o shopper para onde a margem está? Onde ela tem buraco, degrau fraco ou inversão, e quanto vale consertar?**

## 1. Entrada

| Precisa | Exemplo em `dados/` | Se faltar |
|---|---|---|
| SKUs com tamanho, conteúdo (kg/L), embalagem e preço de lista | `produtos.csv`, `vendas_semanais.csv` | Sem conteúdo não há PPA; pedir |
| Preço de prateleira ou como estimá-lo (markup da revenda) | `condicoes_canal.csv` | Usar preço coletado em loja; se não houver, estimar e avisar |
| Volume por SKU e canal | `vendas_semanais.csv` | Pedir pelo menos o volume anual |
| Margem de bolso por SKU | Saída da skill `price-waterfall` | Usar a margem bruta e avisar |
| Elasticidade e substituição entre tamanhos | `produtos.csv`; canibalização da skill `retorno-promocao` | Usar faixas e mostrar cenários |

## 2. Métricas

Por categoria e canal, do menor para o maior tamanho:
- **Preço de prateleira por kg/L.** Estimado como lista × (1 − on-invoice) × (1 + IPI) × (1 + markup da revenda) × (1 + markup do varejo final, se houver).
- **Desconto por kg/L entre degraus** = 1 − (R$/kg do maior ÷ R$/kg do menor).
- **Razão de preço** (absoluto) e **razão de conteúdo** entre degraus.
- **Participação em volume** (kg ou L) e **margem de bolso por kg/L**.

## 3. Passos

1. Montar a escada por categoria num canal de referência e conferir nos outros. **Padrão: a maior rede de supermercados (autosserviço)**, porque é o preço que o shopper usa como régua; declare a escolha. Use a **última lista vigente**, sem desconto promocional, e a margem de bolso **de todos os canais** do SKU.
2. Aplicar as regras de `references/regras-decisao.md` (PP1 a PP7).
3. Para cada problema, desenhar **2 ou 3 jogadas** (lançar, repreçar, tirar ou mudar conteúdo) e simular com `references/simulacao.md`, sempre em três cenários de origem do volume.
4. Recomendar a jogada com o melhor resultado no cenário base que **não seja negativa no conservador**. Se todas forem negativas no conservador, a recomendação é testar, não lançar.
5. Montar a saída (seção 4) seguindo `../price-waterfall/references/visual.md`.

## 4. Saída: layout é requisito

1. **Número-chave:** o valor da melhor jogada (faixa de cenários) e o problema que ela resolve.
2. **Escada por categoria** em pequenos múltiplos: R$/kg ou R$/L por tamanho, com o desconto de cada degrau e a lacuna marcada.
3. **Jogadas simuladas** em barras com a faixa conservador-otimista e o ponto do cenário base. Incluir a jogada intuitiva que perde dinheiro, se houver: ela ensina.
4. **Tabela de margem por kg/L por tamanho**, mostrando para onde o volume deveria ir.
5. **Recomendações** no formato fixo (achado, regra, valor, ação, quando, risco).
6. **Ressalvas** no fim.

## 5. O que não fazer

- Comparar preço por unidade entre tamanhos diferentes; a comparação é sempre por kg/L.
- Lançar um tamanho sem dizer de onde vem o volume. Volume novo sem origem é só otimismo.
- "Consertar" um degrau fraco baixando o preço do tamanho de margem menor, sem rodar a alternativa de subir o tamanho vizinho.
- Reduzir conteúdo sem avisar o consumidor: a mudança de quantidade exige informação clara na embalagem por um período (conferir a norma vigente do Inmetro e do Código de Defesa do Consumidor).

## Vocabulário

Price-pack architecture, escada de preço (price ladder), preço por kg/L, degrau, price point, entrada (opening price point), multipack, lacuna de portfólio, downsizing (shrinkflation), trade-up e trade-down, origem do volume (source of volume), canibalização.
