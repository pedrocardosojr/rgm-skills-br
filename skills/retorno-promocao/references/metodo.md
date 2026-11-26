# Método e fórmulas

Notação: SKU promovido **s**, canal **c**, semanas do evento **W** (duração **d**), as 2 semanas seguintes **W⁺**, irmãos **k** (mesma categoria e canal), conteúdo **g** (kg ou L).

## Margem unitária
O preço de bolso por unidade segue a convenção do `price-waterfall` (sem impostos; off-invoice e custo financeiro sobre o preço de nota). Margem unitária `m = bolso − custo variável`. Na promoção, `m` cai porque o preço de nota cai.

## Baseline
`B_s` = média das unidades nas semanas limpas em [−6, −1] e [d+2, d+7] em torno do evento. **Semana limpa** = sem evento em **nenhum** SKU da mesma categoria × canal (promoção de um irmão contamina a baseline). `m̄_s` é a média da margem unitária nessas semanas. O mesmo vale para cada irmão `k`.

Na borda dos dados, use as semanas limpas que houver. Com menos de 3, marque o evento como **baseline frágil** e trate-o como inconclusivo.

## Componentes (em R$)
- **Margem extra no SKU:** `Σ_W u·m − d·B_s·m̄_s`
- **Efeito nos irmãos:** `Σ_k Σ_W (u_k·m_k − B_k·m̄_k)`. Canibalização % = queda dos irmãos em conteúdo equivalente ÷ incremental do SKU.
- **Pull-forward:** `Σ_{W⁺} (u·m − B_s·m̄_s)`. Pull-forward % = queda em unidades ÷ incremental.
- **Resultado** = margem extra + irmãos + pull-forward − verba fixa.
- **Investimento** = `Σ_W u × (desconto unitário no preço de bolso)` + verba fixa.

## Lift de equilíbrio
`lift_eq = m̄_s × (1 + verba ÷ (m̄_s·B_s·d)) ÷ m_promo − 1`, antes de canibalização e pull-forward. Se o lift obtido for menor, a profundidade não se paga nem no melhor caso.

## Faixa de ruído
Para cada série envolvida (o SKU em W e W⁺ juntos, com `t = d + 2`, e cada irmão em W, com `t = d`), com desvio-padrão semanal **amostral** `σ` (n − 1) das semanas limpas e `n` semanas de baseline:
`Var = Σ (t·σ² + (t·σ)²/n) × m̄²`
O evento é **conclusivo** se `|resultado| > 1,96 × √Var`.

O desvio-padrão inclui a sazonalidade da janela, por isso a faixa é conservadora. Com histórico longo, prefira um modelo de baseline com sazonalidade e use o erro do modelo.

## Quando há dado melhor
- **Grupo de controle** (lojas ou clientes sem a promoção): substitui a baseline e corta a faixa de ruído.
- **Dados de sell-out ou de painel:** separam o pull-forward do consumidor do estoque do varejista (forward buying).
