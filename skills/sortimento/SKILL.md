---
name: sortimento
description: Analisa e otimiza o sortimento de bens de consumo com dados de sell-out por loja. Mede a distribuição numérica e ponderada, a venda por loja, e a incrementalidade de cada SKU (quanto da venda some da categoria quando ele sai, ou seja, a transferência de demanda) com teste de descontinuação e diferença em diferenças. Recomenda onde expandir, onde trocar e onde cortar, com valor em R$. Use quando pedirem "sortimento", "racionalização de SKUs", "cauda longa", "distribuição numérica", "distribuição ponderada", "transferência de demanda", "incrementalidade", "mix obrigatório" ou "planograma".
---

# Sortimento

Cortar um SKU só economiza se a venda dele for para os irmãos; expandir um SKU só vale se ele trouxer venda nova. A pergunta é: **quanto de cada SKU é venda nova para a categoria, e onde ele está faltando?**

## Entrada
- Sell-out mensal (ou semanal) por loja × SKU, com o cadastro das lojas (canal, porte). No exemplo: `dados/sellout_lojas.csv` e `dados/lojas.csv`, com 200 lojas e 12 meses.
- Um **teste de descontinuação**: lojas em que o SKU saiu numa data conhecida (`dados/testes_descontinuacao.csv`). Sem teste, use lojas que nunca tiveram o SKU, sabendo que o resultado sai viesado pelo perfil da loja.
- Margem por unidade (skill `price-waterfall`) e o fator para extrapolar o painel ao total da empresa.

## Métricas
- **Distribuição numérica (DN):** % das lojas que vendem o SKU, por canal.
- **Distribuição ponderada (DP):** % da venda da categoria que está nas lojas que têm o SKU.
- **Venda por loja (rate of sale):** venda do SKU nas lojas que o têm.
- **Incrementalidade:** perda da categoria quando o SKU sai ÷ venda esperada do SKU. Medida por **diferença em diferenças**: a categoria nas lojas tratadas, antes e depois, contra as lojas de controle (com o SKU e sem nenhuma saída na categoria), com intervalo por bootstrap das lojas. A transferência é 1 − incrementalidade.

## Regras
| Código | Situação | Ação |
|---|---|---|
| **S1** | Incrementalidade ≥ 50% e DN abaixo de 80% num canal | **Expandir** a distribuição nesse canal. Valor = lojas faltantes × venda por loja × incrementalidade × margem |
| **S2** | Incrementalidade < 35% e DN < 50% num canal | **Candidato a sair** desse canal: a maior parte da venda migra |
| **S3** | O espaço liberado por S2 pode receber um SKU de S1 | **Trocar** na mesma loja: é o ganho mais rápido |
| **S4** | Intervalo da incrementalidade cruza 50% | Repetir o teste com mais lojas antes de decidir |
| **S5** | SKU com DN acima de 85% em todos os canais | Núcleo do sortimento: mix obrigatório, não entra em teste |

## Saída
Gráfico de incrementalidade × DN com os quadrantes "expandir" e "candidato a corte", a tabela de DN por canal e as recomendações no formato fixo, com o valor extrapolado e a ressalva do painel.

## Cuidados
- Corte não é só volume: confira custo de complexidade, exigência do cliente e o papel do SKU (entrada de preço, lançamento).
- A incrementalidade varia por canal e por formato de loja; com teste suficiente, estime por canal.
- O teste tem que ter controle: comparar só antes e depois mistura sazonalidade.
