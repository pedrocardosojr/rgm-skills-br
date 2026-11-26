# Modelo de preço na transição

Notação, por categoria e ano: preço líquido da indústria **P = 1**; ICMS **i**, PIS/Cofins **p** e IPI **v**, cada um multiplicado pelo fator do ano; CBS + IBS **t**, já com a redução da categoria; Imposto Seletivo **s**.

## Nota fiscal da indústria
```
base_antiga = P / (1 − i − p)          # ICMS e PIS/Cofins por dentro
IPI         = v × base_antiga
IS          = s × P
CBS+IBS     = t × (P + IS)              # por fora; o IS entra na base
nota        = base_antiga + IPI + IS + CBS+IBS
```

## Prateleira
**Varejo com crédito pleno** (regime regular): credita ICMS, PIS/Cofins e CBS/IBS; IPI e IS viram custo.
```
custo_liq  = P + IPI + IS
prateleira = custo_liq × (1 + m) / (1 − i − p) + t × custo_liq × (1 + m)
```
**Varejo sem crédito** (Simples): `prateleira = nota × (1 + m)`. O tributo do Simples sobre a receita dele é ignorado.

O markup **m** cancela no índice: `índice_ano = prateleira_ano / prateleira_2025 × 100`. O ano-base 2025 usa a carga atual (todos os fatores = 1, sem CBS/IBS). Por canal, **pondere os índices** (não os preços) pela fatia da revenda no Simples; no distribuidor, trate a fatia no Simples como o elo final sem crédito.

O IBS de 0,1% de 2027 e 2028 entra como carga, como está no cronograma. O **IS de equilíbrio principal** é o do varejo com crédito pleno; mostre o dos canais mistos só se for muito diferente.

## Valor em disputa e cenários
- Queda da prateleira com P constante: `q = índice/100`. Alta de P que mantém a prateleira: `k = 1/q − 1`.
- Valor em disputa = `k × preço de bolso` do par categoria × canal (do waterfall).
- Elasticidade da marca **e** = `ec` (categoria) + `es` (troca de marca). Padrão: `ec = 0,35 × e`. Calibre com histórico se houver.
- Captura **α**: o preço líquido sobe `α × k`. Com margem de bolso `MB` e preço de bolso `PB`:

| Reação | Margem de bolso nova |
|---|---|
| Concorrência repassa | `(MB + αk·PB) × q^ec × (1+αk)^es` |
| Concorrência captura | `(MB + αk·PB) × (q·(1+αk))^es` |
| Varejo retém (prateleira não muda) | `MB + αk·PB` |

A hipótese é que a empresa é pequena perto da categoria (o preço médio da categoria segue a concorrência). Para um líder, use `e` inteira no cenário "concorrência repassa".

## Simplificações declaradas
- Sem substituição tributária, sem benefícios estaduais e sem regime monofásico, a menos que a carga efetiva seja informada.
- 2026 é neutro: a CBS de 0,9% e o IBS de 0,1% são destacados e compensados.
- O ICMS do varejo usa a mesma alíquota da indústria.
- Não há efeito sobre capital de giro (split payment) nem sobre o saldo credor acumulado; mencione se o cliente tiver crédito acumulado relevante.
