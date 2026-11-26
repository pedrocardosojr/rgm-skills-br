"""Dados de exemplo para as skills de mix e de sortimento (Vale Alto Alimentos, fictícia).

Gera:
- dados/ano_anterior.csv: SKU x canal no ano anterior (unidades, preço líquido médio e custo unitário),
  para a ponte preço-volume-mix contra as 52 semanas de vendas_semanais.csv
- dados/lojas.csv e dados/sellout_lojas.csv: 80 lojas, 12 meses de sell-out por SKU, com sortimento
  diferente por loja e transferência de demanda quando um SKU falta
Reproduzível: semente fixa, só biblioteca padrão. Uso: python3 scripts/gerar_dados_mix_sortimento.py
"""
import csv
import math
import random
from collections import defaultdict
from pathlib import Path

random.seed(7)
D = Path(__file__).resolve().parent.parent / "dados"
rd = lambda n: list(csv.DictReader(open(D / n, encoding="utf-8")))
P = {r["sku"]: r for r in rd("produtos.csv")}
TA = {r["categoria"]: r for r in rd("tributacao_atual.csv")}

# ---------------- ano anterior ----------------
# história: o ano cresceu em volume puxado pelo Atacarejo e pelo 2 L (mix pior), o café ficou mais caro
CRESC_CANAL = {"ATC": 1.14, "RNA": 1.00, "SRG": 0.97, "DIS": 1.05}
CRESC_SKU = {"REF2L": 1.18, "BIS390": 1.15, "CAF250": 0.94, "REF350": 0.96}
REAJ = {"Café": 0.06, "Biscoito": 0.04, "Refrigerante": 0.05}      # reajustes de lista do ano
INFL_CUSTO = {"Café": 0.11, "Biscoito": 0.03, "Refrigerante": 0.04}
agg = defaultdict(lambda: [0, 0.0])
for r in rd("vendas_semanais.csv"):
    s, c, u = r["sku"], r["canal"], int(r["unidades"])
    cat = P[s]["categoria"]; t = (float(TA[cat]["icms_pct"]) + float(TA[cat]["pis_cofins_pct"])) / 100
    nr = u * float(r["preco_lista_unit"]) * (1 - t) * (1 - float(r["desc_on_invoice_pct"]) / 100) * (1 - float(r["desc_promo_pct"]) / 100)
    agg[(s, c)][0] += u; agg[(s, c)][1] += nr
linhas = []
for (s, c), (u, nr) in sorted(agg.items()):
    cat = P[s]["categoria"]
    g = CRESC_CANAL[c] * CRESC_SKU.get(s, 1.0) * math.exp(random.gauss(0, 0.02))
    u25 = round(u / g)
    p26 = nr / u
    p25 = p26 / (1 + REAJ[cat] * 0.85) * math.exp(random.gauss(0, 0.01))   # parte do reajuste se perdeu em desconto
    c25 = float(P[s]["custo_variavel_unit"]) / (1 + INFL_CUSTO[cat])
    linhas.append([s, c, u25, f"{p25:.4f}", f"{c25:.4f}"])
with open(D / "ano_anterior.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["sku", "canal", "unidades", "preco_liquido_unit", "custo_variavel_unit"]] + linhas)

# ---------------- lojas e sell-out ----------------
CANAIS_LOJA = [("ATC", 35), ("RNA", 60), ("SRG", 50), ("TRAD", 55)]   # TRAD = varejo tradicional atendido pelo distribuidor
TAM = {"P": 0.5, "M": 1.0, "G": 1.8}
# velocidade-base (unidades/mês numa loja M) e probabilidade de o SKU estar no sortimento, por canal
VEL = {"CAF250": 90, "CAF500": 260, "CAF1K": 80, "BIS090": 520, "BIS130": 640, "BIS390": 95, "REF350": 330, "REF600": 300, "REF2L": 420}
PROB = {
    "ATC": {"CAF250": 0.55, "CAF500": 1, "CAF1K": 1, "BIS090": 0.6, "BIS130": 1, "BIS390": 1, "REF350": 0.8, "REF600": 0.7, "REF2L": 1},
    "RNA": {"CAF250": 0.9, "CAF500": 1, "CAF1K": 0.85, "BIS090": 0.95, "BIS130": 1, "BIS390": 0.8, "REF350": 0.95, "REF600": 0.9, "REF2L": 1},
    "SRG": {"CAF250": 0.85, "CAF500": 1, "CAF1K": 0.6, "BIS090": 0.9, "BIS130": 0.95, "BIS390": 0.5, "REF350": 0.9, "REF600": 0.85, "REF2L": 0.95},
    "TRAD": {"CAF250": 0.75, "CAF500": 0.9, "CAF1K": 0.25, "BIS090": 0.85, "BIS130": 0.8, "BIS390": 0.15, "REF350": 0.55, "REF600": 0.8, "REF2L": 0.6},
}
# fração da demanda de um SKU ausente que migra para os irmãos da categoria (o resto sai da marca)
TRANSF = {"CAF250": 0.75, "CAF500": 0.55, "CAF1K": 0.80, "BIS090": 0.70, "BIS130": 0.50, "BIS390": 0.85,
          "REF350": 0.30, "REF600": 0.45, "REF2L": 0.70}
SAZ = {"Café": [0.95, 1, 1, 1.08, 1.1, 1.12, 1.12, 1.08, 1, 1, 1, 0.95], "Biscoito": [1.08, 1, 1.1, 1, 1, 1, 1.05, 1, 1, 1.05, 1, 1],
       "Refrigerante": [1.3, 1.35, 1.25, 1.1, 1, 0.85, 0.85, 0.95, 1, 1, 1.12, 1.3]}
MESES = ["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10", "2026-11"]
FATOR_CANAL = {"ATC": 1.6, "RNA": 1.0, "SRG": 0.8, "TRAD": 0.35}
lojas, sell, testes = [], [], []
TESTE = ["CAF250", "CAF1K", "BIS090", "BIS390", "REF350", "REF600"]
n = 0
for canal, qtd in CANAIS_LOJA:
    for _ in range(qtd):
        n += 1
        loja = f"L{n:03d}"
        tam = random.choices(["P", "M", "G"], weights=[0.35, 0.45, 0.2] if canal != "TRAD" else [0.7, 0.3, 0])[0]
        cidade = random.choice(["Curitiba", "Ponta Grossa", "Londrina", "Joinville", "Maringá", "Cascavel"])
        lojas.append([loja, canal, tam, cidade])
        mix = {s: random.random() < PROB[canal][s] for s in P}
        for cat in {p["categoria"] for p in P.values()}:
            skus = [s for s in P if P[s]["categoria"] == cat]
            if not any(mix[s] for s in skus):
                mix[max(skus, key=lambda s: VEL[s])] = True
        efeito_loja = math.exp(random.gauss(0, 0.15))
        # teste de descontinuação: em ~30% das lojas que têm o SKU, ele sai a partir de junho/2026
        saida = {}
        for s in TESTE:
            if mix[s] and random.random() < 0.30:
                saida[s] = 6
                testes.append([loja, s, MESES[6]])
        for m, mes in enumerate(MESES):
            mix_m = {s: mix[s] and not (s in saida and m >= saida[s]) for s in P}
            for s in P:
                if not mix_m[s]:
                    continue
                cat = P[s]["categoria"]; grupo = [k for k in P if P[k]["categoria"] == cat]
                presentes = [k for k in grupo if mix_m[k]]
                extra = sum(VEL[k] * TRANSF[k] for k in grupo if not mix_m[k]) * VEL[s] / sum(VEL[j] for j in presentes)
                u = (VEL[s] + extra) * TAM[tam] * FATOR_CANAL[canal] * SAZ[cat][m] * efeito_loja * math.exp(random.gauss(0, 0.1))
                sell.append([loja, s, mes, int(round(u))])
with open(D / "testes_descontinuacao.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["loja", "sku", "mes_saida"]] + testes)
with open(D / "lojas.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["loja", "canal", "porte", "cidade"]] + lojas)
with open(D / "sellout_lojas.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["loja", "sku", "mes", "unidades"]] + sell)
print(f"ok: {len(linhas)} linhas de ano anterior, {len(lojas)} lojas, {len(sell)} linhas de sell-out")
