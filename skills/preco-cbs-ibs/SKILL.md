---
name: preco-cbs-ibs
description: Simula preço e margem de bens de consumo na transição da reforma tributária brasileira (CBS, IBS e Imposto Seletivo, 2026-2033). Mostra ano a ano o que acontece com a nota e com a prateleira em cada canal, quanto dinheiro fica em disputa entre indústria, varejo e consumidor, e quanto do ganho capturar ou repassar, considerando o crédito do comprador e a reação da concorrência. Use quando pedirem "reforma tributária e preço", "CBS/IBS", "repasse da reforma", "quanto subir ou baixar o preço em 2027", "Imposto Seletivo", "cesta básica" ou "preço por dentro e por fora".
---

# Preço com CBS/IBS

A reforma troca tributos cobrados **por dentro** e cumulativos (ICMS, PIS/Cofins, IPI) por um IVA **por fora** com crédito amplo (CBS + IBS), além de um Imposto Seletivo sobre alguns produtos. Para o RGM, a pergunta é: **quando a carga muda, quem fica com a diferença: a indústria, o varejo ou o consumidor? E quanto disso dá para capturar sem perder volume nem relação com o cliente?**

> Aviso que sempre acompanha a saída: alíquotas e regras são parâmetros a conferir na LC 214/2025, nas resoluções do Senado e na legislação estadual. Isto é simulação de preço, não parecer fiscal.

## 1. Entrada

| Precisa | Exemplo em `dados/` | Se faltar |
|---|---|---|
| Carga atual por categoria (ICMS efetivo, PIS/Cofins, IPI) | `tributacao_atual.csv` | Pedir a carga **efetiva**, com benefícios e ST; alíquota cheia superestima o ganho |
| Regime na reforma (padrão, reduzida, cesta, IS) | `tributacao_reforma.csv` | Classificar pelo NCM, dizendo que é premissa |
| Cronograma e alíquotas por ano | `cronograma_transicao.csv` | Usar o calendário da EC 132/2023 e da LC 214/2025, com CBS + IBS de referência e sensibilidade |
| Fatia da revenda sem crédito pleno (Simples) por canal | `condicoes_canal.csv` | Perguntar; muda o resultado por canal |
| Preço de bolso e margem de bolso por categoria × canal | Saída da skill `price-waterfall` | Usar a receita líquida e a margem bruta, avisando |
| Elasticidade-preço | `produtos.csv` | Usar faixas de mercado (−1,0 a −2,5) e mostrar a sensibilidade |

## 2. O modelo (detalhe em `references/modelo.md`)

1. **Fixar o preço líquido da indústria** (sem impostos) = 1 e calcular, ano a ano, a **nota** e a **prateleira** em cada canal.
2. **Comprador com crédito pleno** (varejo no lucro real): o custo líquido dele é preço líquido + IPI + IS, porque ICMS, PIS/Cofins e CBS/IBS são creditados. A reforma **não muda o custo dele**; o que muda é o imposto na saída dele, e por isso a prateleira pode cair **sem ele perder margem**.
3. **Comprador sem crédito** (Simples, consumidor): o custo é a nota inteira. Quando a nota cai, a queda fica com ele, a menos que a indústria mantenha a nota igual.
4. **Índice de prateleira** (hoje = 100) por canal, ponderando a fatia no Simples. A queda **s** do índice é o **valor em disputa**: k = 1/(1 − s) − 1 é a alta de preço líquido que deixaria a prateleira igual.
5. **Cenários de captura α** (0 = repassar tudo, 0,5 = dividir, 1 = capturar tudo) contra três reações: a concorrência repassa, a concorrência captura e o varejo retém a diferença. O volume reage à elasticidade da categoria (todos mexem juntos) e à elasticidade de troca de marca (só você mexe).
6. **Valor em R$:** margem de bolso de cada cenário − margem de hoje.

Convenções: 2026 é neutro (teste destacado e compensado); o IS entra na base da CBS/IBS; a margem do varejo é um markup sobre o custo líquido (por isso cancela no índice).

## 3. Passos

1. **Validar a carga atual.** Converter a carga por dentro em equivalente por fora: 27,25% por dentro = 37,5% por fora. Essa conta é o ponto que mais engana na comparação com os 26,5%.
2. **Calcular o índice** de nota e de prateleira por categoria × canal × ano (2025 a 2033).
3. **Medir o valor em disputa** (k × preço de bolso) por categoria, canal e ano, e destacar **o primeiro ano em que ele aparece**: 2027 para quem paga PIS/Cofins; 2029 a 2033 para quem só tem ICMS.
4. **Rodar os cenários** de α × reação, com sensibilidade de CBS + IBS (26,5% e 28%) e da alíquota do IS.
5. **Decidir** com `references/regras-decisao.md`, por categoria e por canal.
6. **Montar a saída** (seção 4) seguindo `../price-waterfall/references/visual.md`.

## 4. Saída: layout é requisito

1. **Número-chave:** valor em disputa por ano em R$ e % da margem de bolso, e o ano em que a primeira decisão vence.
2. **Gráfico de linhas** com o índice de prateleira 2025-2033 por categoria, rótulo direto no fim de cada linha e o título com a conclusão.
3. **Tabela de cenários** com o ganho em R$ de "não agir", "plano recomendado" e "capturar tudo" contra as três reações. A célula do plano recomendado vem destacada.
4. **Recomendações** no formato fixo: achado, regra (D1 a D7), valor, ação, quando e risco. É o mesmo formato do `price-waterfall`.
5. **Sensibilidade** em uma linha por parâmetro (alíquota de referência, IS, carga efetiva atual).
6. **Ressalvas** no fim.

## 5. O que não fazer

- Comparar alíquota por dentro com alíquota por fora sem converter.
- Dizer "o varejo vai baixar o preço": no canal com crédito, a queda é uma decisão do varejista, não uma consequência automática.
- Tratar 2026 como ano de mudança de preço. O teste é compensado, e mexer no preço "por causa da reforma" em 2026 é risco de imagem.
- Apresentar "capturar tudo" como plano sem dizer quem precisa aceitar a alta de preço líquido e por quê.
- Esquecer o IS: em produto com Imposto Seletivo, a prateleira pode subir, e a resposta passa por embalagem e portfólio (`price-pack-architecture`), não só por preço.

## Vocabulário

Cálculo por dentro e por fora, não cumulatividade, crédito amplo, split payment, alíquota de referência, cesta básica nacional (alíquota zero), redução de 60%, Imposto Seletivo, regime regular × Simples Nacional, repasse (pass-through), captura de margem, price index contra a concorrência, preço sugerido.
