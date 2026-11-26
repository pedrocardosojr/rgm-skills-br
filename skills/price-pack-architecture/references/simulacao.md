# Simulação de jogadas de PPA

Tudo em kg/L por ano e margem de bolso por kg/L (`m`).

## Lançar um tamanho intermediário N
1. **Preço:** escolha o tamanho e o preço pelo price point de prateleira que ele precisa defender (PP6). Os dois degraus novos têm que ficar menores que o degrau atual, e o preço absoluto de N, abaixo do maior vizinho.
2. **Margem de N:** bolso = lista × (bolso ÷ lista do **vizinho maior de mesmo formato**); custo por kg/L interpolado entre os vizinhos.
3. **Origem do volume**, em 3 cenários:

| Cenário | Tira do maior | Tira do menor | Volume novo (sobre o tirado) |
|---|---|---|---|
| Conservador | 15% | 15% | 0% |
| Base | 12% | 8% | 25% |
| Otimista | 10% | 5% | 50% |

4. **Δ margem** = Σ volume tirado × (m_N − m_origem) + volume novo × m_N.

## Repreçar um tamanho (+x%)
- Volume que ele perde: `V × (1 − (1+x)^e)`.
- Para onde vai a perda, em 3 cenários:

| Cenário | Vai para o vizinho maior | Vai para o vizinho menor | Sai da marca |
|---|---|---|---|
| Conservador | 20% | 10% | 70% |
| Base | 30% | 20% | 50% |
| Otimista | 40% | 25% | 35% |

- **Δ margem** = ganho de preço sobre o volume que fica − margem do volume perdido + margem do volume que migra para os vizinhos.

## Combinar
Uma jogada pode abrir espaço para outra (o tamanho intermediário cria o degrau que torna viável repreçar o maior). Simule a combinação como uma jogada própria.

## Fora da conta (dizer nas ressalvas)
Custo de molde e de linha, taxa de listagem, ruptura no lançamento e tempo até o volume estabilizar.
