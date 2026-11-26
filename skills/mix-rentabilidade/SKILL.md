---
name: mix-rentabilidade
description: Explica e prioriza a rentabilidade de bens de consumo por mix. Monta a ponte de preço, volume, mix e custo (PVM bridge) da receita líquida e do lucro bruto entre dois períodos, a curva ABC por receita e por lucro e a matriz receita × margem por SKU, cliente e canal, com a ação de cada quadrante. Use quando pedirem "PVM", "ponte de margem", "price-volume-mix", "por que a margem caiu", "curva ABC", "Pareto de SKUs", "mix de canal", "rentabilidade por SKU ou cliente" ou ao preparar o fechamento do mês ou o orçamento.
---

# Mix e rentabilidade

A pergunta de todo fechamento: **a receita cresceu, mas por que o lucro não acompanhou? E em quais itens agir primeiro?**

## Entrada
Dois períodos comparáveis (ano contra ano, ou real contra orçamento) por SKU × canal (ou cliente): unidades, receita líquida e custo variável. No exemplo: `dados/ano_anterior.csv` contra as 52 semanas de `vendas_semanais.csv`. Para a matriz, a margem de bolso da skill `price-waterfall`.

## 1. Ponte de preço, volume, mix e custo
Com `u` = unidades, `p` = preço líquido por unidade, `c` = custo por unidade, `m = p − c`, período 0 e 1, item `i`:
- **Volume** = (U₁ − U₀) × m̄₀ (m̄₀ = margem média por unidade no período 0)
- **Mix** = Σ u₁ᵢ × m₀ᵢ − U₁ × m̄₀. Separe em **mix de canal** (com a margem média de cada canal) e **mix de SKU** (o resto).
- **Preço** = Σ u₁ᵢ × (p₁ᵢ − p₀ᵢ)
- **Custo** = −Σ u₁ᵢ × (c₁ᵢ − c₀ᵢ)
A soma fecha exatamente o lucro do período 1. Abra **preço contra custo por categoria**: é ali que aparece o repasse que faltou.

## 2. Curva ABC, em receita e em lucro
Ordene os itens, acumule e classifique: A até 80%, B até 95%, C o resto. Faça **as duas curvas**: um item A em receita e C em lucro é volume que não paga a conta.

## 3. Matriz receita × margem
O eixo x é a participação na receita e o eixo y, a margem de bolso, com as linhas na mediana e na margem média.

| Quadrante | Leitura | Ação |
|---|---|---|
| **Defender** (receita alta, margem alta) | O motor do negócio | Proteger preço e distribuição; nada de promoção profunda |
| **Corrigir** (receita alta, margem baixa) | Onde mora o dinheiro | Condições comerciais (`price-waterfall`), preço e embalagem (`price-pack-architecture`) |
| **Crescer** (receita baixa, margem alta) | Rentável e pequeno | Distribuição (`sortimento`) e visibilidade |
| **Racionalizar** (receita baixa, margem baixa) | Complexidade sem retorno | Testar o corte medindo a incrementalidade (`sortimento`) |

## Saída
Ponte em waterfall com o título-conclusão, matriz com os pontos críticos rotulados, a tabela ABC com os itens que mudam de classe e as recomendações no formato fixo (achado, regra, valor, ação, quando, risco).

## Cuidados
- Mix depende do nível de agregação: diga se é mix de SKU, de canal ou de cliente.
- Compare períodos com a mesma sazonalidade (ano contra ano).
- Inflação de custo não é "efeito preço": separe sempre.
