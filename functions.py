from __future__ import annotations

from typing import List, Tuple

# 1 punktas: Aprašykite tikslo funkciją f(X), lygybinio ir nelygybinių apribojimų funkcijas gi(X) ir hi(X) taip, kad optimizavimo uždavinys būtų formuluojamas min f(X), gi(X)=0, hi(X)≤0.
def tikslo_funkcija(X: Tuple[float, float, float]) -> float:
    """Minimizuojama funkcija: neigiamas dezes turis."""
    x1, x2, x3 = X
    return -(x1 * x2 * x3)


def g(X: Tuple[float, float, float]) -> float:
    """Lygybinis apribojimas: pavirsiaus plotas turi buti 1."""
    x1, x2, x3 = X
    return 2.0 * (x1 * x2 + x2 * x3 + x3 * x1) - 1.0


def h(X: Tuple[float, float, float]) -> List[float]:
    """Nelygybiniai apribojimai x1 >= 0, x2 >= 0, x3 >= 0 uzrasyti kaip h_i(X) <= 0."""
    x1, x2, x3 = X
    return [-x1, -x2, -x3]


def apribojimu_bauda(X: Tuple[float, float, float]) -> float:
    """Kvadratine apribojimu bauda b(X)."""
    bauda = g(X) ** 2
    for hi in h(X):
        bauda += max(0.0, hi) ** 2
    return bauda


# 3 punktas: Aprašykite kvadratinę baudos funkciją, apimančią tikslo funkciją ir apribojimus.
def baudos_funkcija(X: Tuple[float, float, float], r: float) -> float:
    """Kvadratine baudos funkcija B(X,r)=f(X)+1/r*b(X)."""
    if r <= 0:
        raise ValueError("r turi buti > 0")

    return tikslo_funkcija(X) + apribojimu_bauda(X) / r
