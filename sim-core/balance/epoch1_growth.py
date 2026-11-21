"""Таблица скоростей роста эпохи 1 (docs/epoch-1-prokaryotes.md, §3).

Запуск: python3 sim-core/balance/epoch1_growth.py
"""
import numpy as np

P = dict(a=3.0, K=1.0, b=1.5, m=0.02, e=1.0, g=2e-5, d=2e-4, mu_max=1.5)


def growth_rate(r, C, Y, G, p=P):
    """μ = min(μ_max, (Y·I − M) / E_div) для сферической клетки радиуса r."""
    j_tr = p["a"] * r * r * C / (p["K"] + C)   # переносчики, насыщение
    j_diff = p["b"] * r * C                    # диффузионный предел (Berg & Purcell)
    intake = 1 / (1 / j_tr + 1 / j_diff)
    upkeep = p["m"] * r**3 + p["g"] * G
    cost_div = p["e"] * r**3 + p["d"] * G
    return min(p["mu_max"], (Y * intake - upkeep) / cost_div)


def best(C, Y, G):
    radii = np.linspace(0.05, 5, 1000)
    rates = [growth_rate(r, C, Y, G) for r in radii]
    i = int(np.argmax(rates))
    return radii[i], rates[i]


if __name__ == "__main__":
    envs = [("Открытый океан", 0.05), ("Микробный мат", 0.5), ("Богатая среда", 5.0)]
    strategies = [("брожение", 2), ("анаэр. дыхание", 6), ("аэр. дыхание", 30)]
    genomes = [800, 1500, 4000]
    print("μ при оптимальном r; столбцы — геном", genomes)
    for env, C in envs:
        print(f"\n{env} (C={C})")
        for name, Y in strategies:
            cells = " / ".join(f"{best(C, Y, G)[1]:.2f}" for G in genomes)
            print(f"  {name:15s} {cells}")
