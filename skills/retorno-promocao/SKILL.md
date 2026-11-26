---
name: retorno-promocao
description: Mede o retorno de promoções em bens de consumo (post-event analysis). Estima a baseline, o volume incremental, a canibalização entre SKUs e o pull-forward (antecipação de compra), e calcula o resultado em margem de bolso e o ROI de cada evento, com uma faixa de ruído que separa o que é conclusivo do que não é. Recomenda cortar, redesenhar, testar ou repetir, com valor em R$. Use quando pedirem "retorno de promoção", "ROI de promoção", "trade promotion", "a promoção se pagou?", "calendário promocional", "verba de encarte" ou "post-event analysis".
---

# Retorno de promoção

Volume que sobe não prova que a promoção funcionou. A pergunta é: **quanto de margem a promoção criou depois de descontar o volume que ia acontecer de qualquer jeito, o que ela tirou dos outros SKUs, o que ela só antecipou e o que se pagou de verba? E esse número é maior que o ruído?**

## 1. Entrada

| Precisa | Exemplo em `dados/` | Se faltar |
|---|---|---|
| Vendas semanais por SKU × canal (ou cliente), com marcação do evento | `vendas_semanais.csv` | Semanal é o mínimo; vendas mensais não medem promoção |
| Cadastro dos eventos: SKU, canal, início, duração, mecânica, desconto, verba fixa | `promocoes.csv` | Pedir; sem a verba fixa, o ROI fica superestimado |
| Margem unitária no preço normal e no preço promocional | Lógica da skill `price-waterfall` | Usar a margem bruta e avisar |
| Família de substitutos (mesma categoria e canal) e conteúdo (kg/L) | `produtos.csv` | Perguntar quais SKUs competem entre si |

## 2. Método (detalhe e fórmulas em `references/metodo.md`)

1. **Baseline:** média das semanas limpas de até 6 semanas antes e até 6 semanas depois do evento. Excluir as 2 semanas logo depois e qualquer semana com outro evento. Com 2 anos ou mais de dados, use um modelo com sazonalidade.
2. **Incremental bruto** = unidades na promoção − baseline.
3. **Canibalização:** queda dos irmãos (mesma categoria e canal) contra a baseline deles, em conteúdo equivalente.
4. **Pull-forward:** queda do próprio SKU nas 2 semanas seguintes contra a baseline.
5. **Resultado** = margem extra do SKU na promoção + efeito nos irmãos + efeito no pós-promoção − verba fixa.
6. **Investimento** = custo do desconto (no preço de bolso) + verba fixa. **ROI** = resultado ÷ investimento.
7. **Ruído:** desvio-padrão do resultado a partir da variação semanal das semanas limpas. Um evento é **conclusivo** quando o |resultado| passa de 1,96 desvio. Dentro da faixa, os dados não dizem se a promoção ganhou ou perdeu.
8. **Lift de equilíbrio:** o lift que a promoção precisaria para empatar com a baseline, já pagando a verba. Compare com o lift obtido.

## 3. Passos

1. Validar o cadastro: todo evento tem que aparecer nas vendas, e evento sobreposto no mesmo SKU × canal precisa ser apontado e tratado junto.
2. Calcular os componentes do método para cada evento.
3. Classificar cada evento: **destrói margem** (negativo e conclusivo), **se paga** (positivo e conclusivo) ou **inconclusivo**.
4. Aplicar as regras de `references/regras-decisao.md` e agrupar eventos com a mesma causa (por exemplo, "2 L com desconto profundo").
5. Montar a saída (seção 4) seguindo `../price-waterfall/references/visual.md`.

## 4. Saída: layout é requisito

1. **Número-chave:** investimento total, resultado total e quantos eventos destroem margem com segurança.
2. **Ranking dos eventos** em barras horizontais com a faixa de ruído: vermelho = destrói com segurança, cinza = inconclusivo, azul = se paga com segurança.
3. **Anatomia de um evento** típico em waterfall (margem extra → canibalização → pull-forward → verba → resultado). Escolha um com lift alto e resultado negativo: é o que convence.
4. **Recomendações** no formato fixo (achado, regra, valor, ação, quando, risco), agrupadas por causa.
5. **Ressalvas** no fim.

## 5. O que não fazer

- Chamar lift de sucesso. Um lift de 158% pode perder R$ 60 mil.
- Medir a canibalização só no SKU vizinho, ou o pull-forward só em 1 semana, quando o item é estocável.
- Decidir sobre eventos inconclusivos como se fossem certos. Eles viram teste, não corte.
- Esquecer o que não está no dado: exigência contratual de calendário, tráfego para a loja e lançamento. Diga isso nas ressalvas e não invente o valor.

## Vocabulário

Baseline, lift, incremental, canibalização, halo, pull-forward (antecipação, forward buying), profundidade de desconto, mecânica (TPR, encarte, ponto extra, leve 3 pague 2), trade spend, ROI promocional, pay-for-performance, post-event analysis, grupo de controle.
