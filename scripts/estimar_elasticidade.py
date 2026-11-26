"""Estima a elasticidade-preço de curto prazo por SKU x canal com pooling parcial (Bayes empírico).

Modelo por par SKU x canal:  ln(unidades) = a + b * ln(preço pago) + efeito do mês + erro
- preço pago = preço de lista vigente x (1 - desconto promocional)
- ficam fora: semanas com promoção de outro SKU da mesma categoria no canal (canibalização),
  as 2 semanas depois de uma promoção do próprio SKU (pull-forward) e eventos com encarte ou
  ponto extra (a mecânica infla o volume além do preço)
Pooling: cada b é puxado para a média da categoria na proporção da sua incerteza
(DerSimonian-Laird). Par com pouca variação de preço herda mais da categoria.

Uso: python3 scripts/estimar_elasticidade.py [pasta_dados] [saida.csv]
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

D = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "dados"
SAIDA = Path(sys.argv[2]) if len(sys.argv) > 2 else None
rd = lambda n: list(csv.DictReader(open(D / n, encoding="utf-8")))
P = {r["sku"]: r for r in rd("produtos.csv")}
PROMO = {r["evento_id"]: r for r in rd("promocoes.csv")}
V = defaultdict(list)
for r in rd("vendas_semanais.csv"):
    V[(r["sku"], r["canal"])].append(r)
semanas = sorted({r["semana"] for v in V.values() for r in v})
idx = {s: i for i, s in enumerate(semanas)}

# semanas "sujas" por categoria x canal e por SKU x canal
evento_cat = defaultdict(set)
pos_evento = defaultdict(set)
for (s, c), rows in V.items():
    for r in rows:
        if r["evento_id"]:
            evento_cat[(P[s]["categoria"], c)].add((idx[r["semana"]], s))
            i = idx[r["semana"]]
            pos_evento[(s, c)].update({i + 1, i + 2})

est = {}
for (s, c), rows in V.items():
    cat = P[s]["categoria"]
    y, x, mes = [], [], []
    for r in rows:
        i = idx[r["semana"]]
        if any(j == i and k != s for j, k in evento_cat[(cat, c)]):
            continue
        if i in pos_evento[(s, c)] and not r["evento_id"]:
            continue
        if r["evento_id"] and PROMO[r["evento_id"]]["mecanica"] != "TPR":
            continue
        preco = float(r["preco_lista_unit"]) * (1 - float(r["desc_promo_pct"]) / 100)
        y.append(np.log(int(r["unidades"])))
        x.append(np.log(preco))
        mes.append(int(r["semana"][5:7]))
    tpr = sum(1 for r in rows if r["evento_id"] and PROMO[r["evento_id"]]["mecanica"] == "TPR")
    if tpr == 0:  # sem variação de preço própria além do reajuste de lista: não identifica
        est[(s, c)] = dict(b=None, se=None, n=len(y), cat=cat)
        continue
    meses = sorted(set(mes))
    X = np.column_stack([np.ones(len(x)), x] + [[1.0 if m == mm else 0.0 for m in mes] for mm in meses[1:]])
    y = np.array(y)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    gl = len(y) - X.shape[1]
    s2 = res @ res / gl
    cov = s2 * np.linalg.pinv(X.T @ X)
    est[(s, c)] = dict(b=beta[1], se=float(np.sqrt(cov[1, 1])), n=len(y), cat=cat,
                       var_preco=float(np.std(x)))

# pooling parcial por categoria (DerSimonian-Laird)
por_cat = defaultdict(list)
for k, e in est.items():
    por_cat[e["cat"]].append(k)
for cat, todos in por_cat.items():
    # nível 1: canais do mesmo SKU compartilham a elasticidade (média ponderada pela precisão)
    skus = sorted({k[0] for k in todos})
    sku_b, sku_v = {}, {}
    for s in skus:
        ks = [k for k in todos if k[0] == s and est[k]["b"] is not None]
        if ks:
            w = np.array([1 / est[k]["se"] ** 2 for k in ks]); b = np.array([est[k]["b"] for k in ks])
            sku_b[s] = (w * b).sum() / w.sum(); sku_v[s] = 1 / w.sum()
    # nível 2: SKUs da categoria (DerSimonian-Laird), com a dispersão real entre tamanhos
    ss = list(sku_b); b = np.array([sku_b[s] for s in ss]); v = np.array([sku_v[s] for s in ss])
    w = 1 / v; mu_fe = (w * b).sum() / w.sum(); q = (w * (b - mu_fe) ** 2).sum()
    tau2 = max(0.0, (q - (len(ss) - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if len(ss) > 1 else 0.0
    w2 = 1 / (v + tau2); mu = (w2 * b).sum() / w2.sum(); se_mu = np.sqrt(1 / w2.sum())
    for k in todos:
        e = est[k]; s = k[0]
        if s in sku_b and tau2 > 0:
            peso = (1 / sku_v[s]) / (1 / sku_v[s] + 1 / tau2)
            bp = peso * sku_b[s] + (1 - peso) * mu; sp = np.sqrt(1 / (1 / sku_v[s] + 1 / tau2))
        elif s in sku_b:
            peso, bp, sp = 0.0, mu, se_mu
        else:  # SKU sem variação de preço própria: herda a categoria, com a dispersão entre SKUs
            peso, bp, sp = 0.0, mu, np.sqrt(se_mu ** 2 + tau2)
        e.update(b_pool=bp, se_pool=float(sp), peso_proprio=peso, media_cat=mu, se_cat=se_mu, tau=np.sqrt(tau2))

linhas = []
for (s, c), e in sorted(est.items()):
    linhas.append([s, c, e["cat"], e["n"], "" if e["b"] is None else round(e["b"], 2), "" if e["se"] is None else round(e["se"], 2), round(e["b_pool"], 2), round(e["se_pool"], 2),
                   round(e["peso_proprio"], 2), round(e["media_cat"], 2)])
cab = ["sku", "canal", "categoria", "semanas_usadas", "elasticidade_par", "erro_padrao_par", "elasticidade_pooled",
       "erro_padrao_pooled", "peso_do_proprio_dado", "media_categoria"]
if SAIDA:
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([cab] + linhas)
for cat, ks in por_cat.items():
    e = est[ks[0]]
    print(f"{cat}: média {e['media_cat']:.2f} (±{1.96 * e['se_cat']:.2f}), dispersão real entre SKUs (tau) {e['tau']:.2f}")
for l in linhas:
    print(*l)
