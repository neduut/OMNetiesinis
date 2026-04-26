from __future__ import annotations

import math
from typing import Dict, List, Tuple

from functions import baudos_funkcija, g, h, tikslo_funkcija
from simpleksas2lab import simpleksas

Point = Tuple[float, float, float]


def tirti_r_itaka(X: Point) -> None:
    print("\nBaudos funkcijos itaka pagal r:")
    for r in [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]:
        print(f"  r={r:<8g} -> B(X,r)={baudos_funkcija(X, r): .8f}")


def optimizuoti_seka(X_pradzia: List[float]) -> List[Dict]:
    """Sprendzia baudos uzdaviniu seka su mazejanciu r ir warm-start."""
    r_seka = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]
    rezultatai: List[Dict] = []
    current = X_pradzia.copy()
    r0 = r_seka[0]

    for etapas, r in enumerate(r_seka, start=1):
        iter_koef = max(1, int(math.sqrt(r0 / r)))
        max_iteracijos = 2000 * iter_koef
        tolerancija = 1e-6 * min(1.0, r / r0)

        sprendinys, iteracijos, kvietimai = simpleksas(
            lambda X: baudos_funkcija(X, r),
            current,
            max_iteracijos=max_iteracijos,
            tolerancija=tolerancija,
        )

        f_reiksme = tikslo_funkcija(tuple(sprendinys))
        g_reiksme = g(tuple(sprendinys))
        h_reiksmes = h(tuple(sprendinys))
        b_reiksme = g_reiksme**2 + sum(max(0.0, hi) ** 2 for hi in h_reiksmes)

        rezultatai.append(
            {
                "etapas": etapas,
                "r": r,
                "sprendinys": sprendinys,
                "f": f_reiksme,
                "b": b_reiksme,
                "B": baudos_funkcija(tuple(sprendinys), r),
                "iteracijos": iteracijos,
                "kvietimai": kvietimai,
                "tolerancija": tolerancija,
                "max_iteracijos": max_iteracijos,
            }
        )

        current = sprendinys.copy()

    return rezultatai


def _spausdinti_rezultatus(vardas: str, rezultatai: List[Dict]) -> None:
    print("\n" + "=" * 84)
    print(f"Pradinis taskas: {vardas}")
    print("=" * 84)

    for r in rezultatai:
        x = r["sprendinys"]
        print(
            f"Etapas {r['etapas']:2d}: r={r['r']:<8g} "
            f"x=({x[0]: .8f}, {x[1]: .8f}, {x[2]: .8f}) "
            f"f={r['f']: .8f} b={r['b']: .3e} B={r['B']: .8f} "
            f"iter={r['iteracijos']:4d} kvietimai={r['kvietimai']:5d}"
        )

    g_final = rezultatai[-1]
    x = g_final["sprendinys"]
    print("-" * 84)
    print(
        f"Galutinis: x=({x[0]: .8f}, {x[1]: .8f}, {x[2]: .8f}), "
        f"f={g_final['f']: .8f}, b={g_final['b']:.3e}, r={g_final['r']:g}"
    )


def palyginimas() -> None:
    # stud knygeles nr: 2412927 -> a=9, b=2, c=7
    X0 = [0.0, 0.0, 0.0]
    X1 = [1.0, 1.0, 1.0]
    Xm = [0.9, 0.2, 0.7]

    rez0 = optimizuoti_seka(X0)
    rez1 = optimizuoti_seka(X1)
    rezm = optimizuoti_seka(Xm)

    _spausdinti_rezultatus("X0", rez0)
    _spausdinti_rezultatus("X1", rez1)
    _spausdinti_rezultatus("Xm", rezm)

    print("\n" + "=" * 84)
    print("Palyginimas")
    print("=" * 84)
    for vardas, rezultatai in [("X0", rez0), ("X1", rez1), ("Xm", rezm)]:
        final = rezultatai[-1]
        x = final["sprendinys"]
        print(
            f"{vardas}: x=({x[0]: .8f}, {x[1]: .8f}, {x[2]: .8f}), "
            f"f={final['f']: .8f}, iter={sum(r['iteracijos'] for r in rezultatai)}, "
            f"kvietimai={sum(r['kvietimai'] for r in rezultatai)}"
        )


if __name__ == "__main__":
    tirti_r_itaka((0.0, 0.0, 0.0))
    palyginimas()
