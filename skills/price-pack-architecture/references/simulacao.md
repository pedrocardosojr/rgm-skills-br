# Simulação de jogadas de PPA

Tudo em kg/L por ano e margem de bolso por kg/L (`m`).

## Lançar um tamanho intermediário N
1. **Preço:** posicione o R$/kg/L de N entre os vizinhos e confira os degraus resultantes com PP2 a PP4. O preço absoluto de N tem que ficar abaixo do maior vizinho.
2. **Margem de N:** bolso = lista × (bolso ÷ lista do vizinho mais parecido); custo por kg/L interpolado entre os vizinhos.
3. **Origem do volume**, em 3 cenários:

| Cenário | Tira do maior | Tira do menor | Volume novo (sobre o tirado) |
|---|---|---|---|
| Conservador | 15% | 15% | 0% |
| Base | 12% | 8% | 25% |
| Otimista | 10% | 5% | 50% |

4. **Δ margem** = Σ volume tirado × (m_N − m_origem) + volume novo × m_N.

## Repreçar um tamanho (+x%)
- Volume que ele perde: `V × (1 − (1+x)^e)`.
- Para onde vai a perda: defina frações para cada vizinho (por exemplo, 30% para o multipack, 20% para o menor, 50% sai da marca) em 3 cenários.
- **Δ margem** = ganho de preço sobre o volume que fica − margem do volume perdido + margem do volume que migra para os vizinhos.

## Combinar
Uma jogada pode abrir espaço para outra (o tamanho intermediário cria o degrau que torna viável repreçar o maior). Simule a combinação como uma jogada própria.

## Fora da conta (dizer nas ressalvas)
Custo de molde e de linha, taxa de listagem, ruptura no lançamento e tempo até o volume estabilizar.
