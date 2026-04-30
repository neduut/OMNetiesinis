from __future__ import annotations

import math
from typing import Dict, List, Tuple

from functions import apribojimu_bauda, baudos_funkcija, g, h, tikslo_funkcija
from simpleksas2lab import simpleksas

Point = Tuple[float, float, float]


def _fmt(value: float, decimals: int = 4) -> str:
    if abs(value) < 0.5 * 10 ** (-decimals):
        return "0"

    text = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def gauti_pradinius_taskus() -> Dict[str, List[float]]:
    # stud knygeles nr: 2412927 -> a=9, b=2, c=7
    return {
        "X0": [0.0, 0.0, 0.0],
        "X1": [1.0, 1.0, 1.0],
        "Xm": [0.9, 0.2, 0.7],
    }


def gauti_r_seka() -> List[float]:
    r0 = 1.0
    beta = 0.3
    r_min = 0.001

    r_seka: List[float] = []
    r = r0

    while r > r_min:
        r_seka.append(r)
        r *= beta

    r_seka.append(r_min)
    return r_seka

# 2 punktas: Apskaičiuokite funkcijų f(X), gi(X), hi(X) reikšmes taškuose X0=(0,0,0), X1=(1,1,1) ir Xm=(a/10,b/10,c/10), čia a,b,c – studento knygelės numerio “2x1xabc” skaitmenys.
def spausdinti_f_g_h_taskuose(taskai: Dict[str, List[float]]) -> None:
    """2 punktas: f(X), g(X), h(X) reiksmes taskuose X0, X1 ir Xm."""
    print("\n---- 2) f(X), g(X), h(X) reiksmes taskuose ----")
    for vardas, taskas in taskai.items():
        X = tuple(taskas)
        f_reiksme = tikslo_funkcija(X)
        g_reiksme = g(X)
        h_reiksmes = h(X)
        print(
            f"- {vardas}: X=({_fmt(X[0])}, {_fmt(X[1])}, {_fmt(X[2])}) "
            f"f={_fmt(f_reiksme, 6)} g={_fmt(g_reiksme, 6)} "
            f"h=[{_fmt(h_reiksmes[0], 6)}, {_fmt(h_reiksmes[1], 6)}, {_fmt(h_reiksmes[2], 6)}]"
        )


def tirti_r_itaka(X: Point, tasko_vardas: str) -> None:
    print(f"\n---- 3) Baudos funkcija B(X,r) pagal r, kai X = {tasko_vardas} ----")
    for r in gauti_r_seka():
        print(f"- r={r:.6g} B(X,r)={_fmt(baudos_funkcija(X, r), 8)}")


# 5 punktas: Minimizuokite baudos funkciją praeitame laboratoriniame darbe sukurtu optimizavimo be apribojimų algoritmu sprendžiant optimizavimo uždavinių seką su mažėjančia parametro r seka, kai pirmasis sekos uždavinys optimizuojamas pradedant iš taškų X0, X1 ir Xm, o kiekvieno paskesnio uždavinio pradinis taškas yra ankstesnio uždavinio sprendinys.
def optimizuoti_seka(X_pradzia: List[float]) -> List[Dict]:
    """Sprendzia baudos uzdaviniu seka su mazejanciu r ir warm-start."""
    r_seka = gauti_r_seka()
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
        b_reiksme = apribojimu_bauda(tuple(sprendinys))

        rezultatai.append(
            {
                "etapas": etapas,
                "r": r,
                "sprendinys": sprendinys,
                "f": f_reiksme,
                "b": b_reiksme,
                "B": f_reiksme + b_reiksme / r,
                "iteracijos": iteracijos,
                "kvietimai": kvietimai,
                "tolerancija": tolerancija,
                "max_iteracijos": max_iteracijos,
            }
        )

        current = sprendinys.copy()

    return rezultatai


def _spausdinti_rezultatus(vardas: str, rezultatai: List[Dict], numeris: str) -> None:
    print(f"\n---- {numeris}) Minimizavimo rezultatai pradeti is {vardas} ----")
    for r in rezultatai:
        x = r["sprendinys"]
        print(
            f"- Etapas {r['etapas']:d}: r={r['r']:.6g} x=({_fmt(x[0], 6)}, {_fmt(x[1], 6)}, {_fmt(x[2], 6)}) "
            f"f={_fmt(r['f'], 8)} B={_fmt(r['B'], 8)} iter={r['iteracijos']:d} kvietimai={r['kvietimai']:d}"
        )

    g_final = rezultatai[-1]
    x = g_final["sprendinys"]
    print(f"- Galutinis: x=({x[0]:.8f}, {x[1]:.8f}, {x[2]:.8f}) f={g_final['f']:.8f} b={g_final['b']:.3e} r={g_final['r']:g}")


# 6 punktas: Palyginkite rezultatus: gauti sprendiniai, rastas funkcijos minimumo įvertis, atliktų žingsnių ir funkcijų skaičiavimų skaičius priklausomai nuo pradinio taško.
def _spausdinti_pradiniu_tasku_palyginima(rezultatai_pag_al_taska: Dict[str, List[Dict]]) -> None:
    """Isveda galutini palyginima pagal pradinius taskus."""
    print("\n---- 5) Palyginimas pagal pradini taska ----")
    for vardas, etapai in rezultatai_pag_al_taska.items():
        galutinis = etapai[-1]
        x = galutinis["sprendinys"]
        f_min_ivertis = galutinis["f"]
        bendri_zingsniai = sum(e["iteracijos"] for e in etapai)
        bendri_f_skaiciavimai = sum(e["kvietimai"] for e in etapai)
        print(f"- {vardas}: x=({x[0]:.6f}, {x[1]:.6f}, {x[2]:.6f}) f={f_min_ivertis:.8f} zingsniai={bendri_zingsniai} f_skaiciavimai={bendri_f_skaiciavimai}")


def palyginimas() -> None:
    taskai = gauti_pradinius_taskus()
    X0 = taskai["X0"]
    X1 = taskai["X1"]
    Xm = taskai["Xm"]

    rez0 = optimizuoti_seka(X0)
    rez1 = optimizuoti_seka(X1)
    rezm = optimizuoti_seka(Xm)

    _spausdinti_rezultatus("X0", rez0, "4.1")
    _spausdinti_rezultatus("X1", rez1, "4.2")
    _spausdinti_rezultatus("Xm", rezm, "4.3")

    _spausdinti_pradiniu_tasku_palyginima({"X0": rez0, "X1": rez1, "Xm": rezm})


if __name__ == "__main__":
    taskai = gauti_pradinius_taskus()
    spausdinti_f_g_h_taskuose(taskai)
    tirti_r_itaka(tuple(taskai["X0"]), "X0")
    palyginimas()
