---
name: price-waterfall
description: Monta o price waterfall de bens de consumo, do preço de lista ao preço de bolso (pocket price) e à margem de bolso, por canal, SKU e cliente. Inclui descontos on-invoice e promocionais, rebate, verba de contrato e de promoção, bonificação, frete e custo financeiro do prazo. Diagnostica onde a margem vaza com regras explícitas e devolve recomendações priorizadas em R$. Use quando pedirem "price waterfall", "cascata de preço", "pocket price", "onde a margem vaza", "quanto custa cada canal", "revisar política comercial" ou ao preparar uma negociação anual com cliente.
---

# Price waterfall

O waterfall mostra quanto do preço de lista chega de fato ao bolso da indústria e quem leva cada pedaço. A pergunta de negócio é sempre: **onde a margem vaza, quanto vale fechar o vazamento e o que fazer primeiro?**

## 1. Entrada

Precisa de vendas no grão SKU × canal (ou cliente) × período e das condições comerciais. Os dados de exemplo em `dados/` seguem este formato (ver `dados/DICIONARIO.md`):

| Precisa | Exemplo em `dados/` | Se faltar |
|---|---|---|
| Unidades e preço de lista vigente | `vendas_semanais.csv` | Sem isso não há análise; pedir |
| Descontos na nota (on-invoice, promoção) | `vendas_semanais.csv` | Usar a política do canal e avisar |
| Condições fora da nota (rebate, verbas, bonificação, frete, prazo) | `condicoes_canal.csv`, `condicoes_especiais.csv`, `promocoes.csv` | Pedir; sem isso é só o waterfall da nota, e isso tem que ser dito |
| Custo variável unitário | `produtos.csv` | Parar na margem de bolso sem custo e avisar |
| Impostos sobre venda | `tributacao_atual.csv` | Perguntar se os preços já estão sem impostos |

Com dados do usuário, mapeie as colunas para estes papéis e **diga em uma linha o mapeamento e as premissas** antes de calcular.

## 2. Convenções (não mudar no meio)

- **Tudo sem impostos.** O preço de lista com ICMS e PIS/Cofins por dentro é convertido antes do primeiro degrau: `lista sem impostos = lista × (1 − ICMS − PIS/Cofins)`. O IPI é cobrado por fora e não entra. Imposto não é vazamento comercial: ele fica fora do waterfall, e quem trata dele é a skill `preco-cbs-ibs`.
- **Ordem dos degraus:**
  1. Preço de lista
  2. − Desconto on-invoice (política + condição especial)
  3. − Desconto promocional
  4. **= Preço de nota**
  5. − Rebate
  6. − Verba de contrato
  7. − Verba de promoção (R$ fixos por evento)
  8. − Bonificação
  9. − Frete
  10. − Custo financeiro do prazo
  11. **= Preço de bolso**
  12. − Custo variável
  13. **= Margem de bolso**
- O on-invoice da venda **já inclui** a condição especial quando houver; não some de novo.
- "Média do canal" e "média da empresa" são sempre **ponderadas** (o agregado), nunca a média simples dos pares.
- Os percentuais off-invoice incidem sobre o **preço de nota**. A verba de promoção entra em R$ no par SKU × canal do evento.
- **Custo financeiro** = taxa mensal × prazo em dias ÷ 30 × preço de nota.
- **Vazamento** = 1 − preço de bolso ÷ preço de lista. **Margem de bolso %** = margem de bolso ÷ preço de bolso.

## 3. Passos

1. **Validar.** Some as unidades e a receita a preço de lista por canal e por mês e confira se fazem sentido (sem semana zerada, sem preço negativo). Se houver DRE, confira a receita líquida com ela; uma diferença acima de 2% precisa ser explicada antes de seguir.
2. **Calcular por SKU × canal**, em R$ no período, cada degrau da seção 2.
3. **Consolidar** em total, canal e SKU. A soma dos degraus tem que fechar exatamente lista − bolso; se não fechar, há erro, e não se segue em frente.
4. **Diagnosticar** com as regras de `references/regras-diagnostico.md`. Cada regra que dispara vira um achado com o valor em R$ por ano.
5. **Priorizar** os achados por valor × facilidade (seção 4).
6. **Montar a saída** (seção 5) seguindo `references/visual.md`.

## 4. Recomendação estruturada

Cada achado sai neste formato, sem texto solto:

| Campo | Conteúdo |
|---|---|
| Achado | Uma frase com o número: "REF2L no Atacarejo vaza 28%, 6 p.p. acima do canal" |
| Causa | A rubrica que explica pelo menos metade do desvio |
| Regra | O código da regra que disparou (R1 a R7) |
| Valor | R$ por ano em jogo (margem de bolso recuperável) |
| Ação | O verbo e o objeto: "converter a bonificação em desconto condicionado a volume" |
| Quando | Na próxima renovação, já (decisão unilateral) ou depois de testar |
| Risco | O que pode dar errado (perda de volume, reação do cliente) e como medir |

Prioridade: **1** = valor alto e decisão interna; **2** = valor alto e depende de negociação; **3** = valor baixo. Feche com o total em R$ e o peso sobre a margem de bolso ("R$ 0,55 mi por ano, +2,3% de margem de bolso").

## 5. Saída: layout é requisito

Na ordem, em uma página:

1. **Número-chave:** quanto da lista não chega ao bolso, em R$ e em %, e quanto disso é recuperável.
2. **Gráfico de waterfall** do total, com o título dizendo a conclusão.
3. **Mapa SKU × canal:** desvio do vazamento em relação à média do canal, em escala divergente.
4. **Tabela de recomendações** (seção 4), ordenada por prioridade.
5. **Ressalvas no fim**, curtas: premissas, dados que faltaram e o que não foi considerado.

As especificações de cor, rótulo e formato estão em `references/visual.md`. A análise sem o visual não está pronta.

## 6. O que não fazer

- Não chamar imposto de vazamento nem misturar preço com e sem impostos no mesmo gráfico.
- Não recomendar "reduzir desconto" sem dizer qual, de quem, quanto vale e quando.
- Não comparar vazamento entre canais sem olhar a margem de bolso: um canal pode vazar mais e dar mais margem.
- Não ler a verba de promoção como problema sem antes medir o retorno; isso é da skill `retorno-promocao`.

## Vocabulário

Preço de lista, preço de nota (invoice price), preço de bolso (pocket price), margem de bolso (pocket margin), on-invoice e off-invoice, rebate, verba de contrato (enxoval, aniversário, ponto extra), bonificação, pay-for-performance, price band (dispersão do preço de bolso entre clientes), cost-to-serve.
