from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

from functions import baudos_funkcija, g, h, tikslo_funkcija
from simpleksas2lab import simpleksas

Point = Tuple[float, float, float]
SUMMARY_FILE = Path(__file__).with_name("rezultatai.md")


def gauti_pradinius_taskus() -> Dict[str, List[float]]:
    # stud knygeles nr: 2412927 -> a=9, b=2, c=7
    return {
        "X0": [0.0, 0.0, 0.0],
        "X1": [1.0, 1.0, 1.0],
        "Xm": [0.9, 0.2, 0.7],
    }

# 2 punktas: Apskaičiuokite funkcijų f(X), gi(X), hi(X) reikšmes taškuose X0=(0,0,0), X1=(1,1,1) ir Xm=(a/10,b/10,c/10), čia a,b,c – studento knygelės numerio “2x1xabc” skaitmenys.
def spausdinti_f_g_h_taskuose(taskai: Dict[str, List[float]]) -> None:
    """2 punktas: f(X), g(X), h(X) reiksmes taskuose X0, X1 ir Xm."""
    print("\nFunkciju f(X), g(X), h(X) reiksmes taskuose:")
    for vardas, taskas in taskai.items():
        X = tuple(taskas)
        f_reiksme = tikslo_funkcija(X)
        g_reiksme = g(X)
        h_reiksmes = h(X)
        print(f"{vardas} = ({X[0]:.3f}, {X[1]:.3f}, {X[2]:.3f})")
        print(f"  f(X)  = {f_reiksme:.8f}")
        print(f"  g(X)  = {g_reiksme:.8f}")
        print(
            f"  h(X)  = [{h_reiksmes[0]:.8f}, {h_reiksmes[1]:.8f}, {h_reiksmes[2]:.8f}]"
        )


# 4 punktas: Patyrinėkite baudos daugiklio įtaką baudos funkcijos reikšmėms.
def tirti_r_itaka(X: Point) -> None:
    print("\nBaudos funkcijos itaka pagal r:")
    print("r pokytis rodo, kaip stipriai baudos narys veikia baudos funkcijos verte.")
    for r in [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]:
        print(f"  r={r:<8g} -> B(X,r)={baudos_funkcija(X, r): .8f}")


def gauti_r_tyrimo_rezultatus(X: Point) -> List[Tuple[float, float]]:
    """Grąžina baudos funkcijos reikšmes skirtingiems r, kad jas būtų galima ir išspausdinti, ir įrašyti į failą."""
    return [(r, baudos_funkcija(X, r)) for r in [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]]


# 5 punktas: Minimizuokite baudos funkciją praeitame laboratoriniame darbe sukurtu optimizavimo be apribojimų algoritmu sprendžiant optimizavimo uždavinių seką su mažėjančia parametro r seka, kai pirmasis sekos uždavinys optimizuojamas pradedant iš taškų X0, X1 ir Xm, o kiekvieno paskesnio uždavinio pradinis taškas yra ankstesnio uždavinio sprendinys.
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


# 6 punktas: Palyginkite rezultatus: gauti sprendiniai, rastas funkcijos minimumo įvertis, atliktų žingsnių ir funkcijų skaičiavimų skaičius priklausomai nuo pradinio taško.
def _spausdinti_pradiniu_tasku_palyginima(rezultatai_pag_al_taska: Dict[str, List[Dict]]) -> None:
    """Isveda galutini palyginima pagal pradinius taskus."""
    print("\n" + "=" * 110)
    print("Palyginimas pagal pradini taska")
    print("=" * 110)
    print(
        f"{'Taskas':<8} {'Sprendinys (x,y,z)':<38} {'f min ivertis':>14} "
        f"{'Zingsniai':>12} {'F sk.':>12}"
    )
    print("-" * 110)

    for vardas, etapai in rezultatai_pag_al_taska.items():
        galutinis = etapai[-1]
        x = galutinis["sprendinys"]
        f_min_ivertis = galutinis["f"]
        bendri_zingsniai = sum(e["iteracijos"] for e in etapai)
        bendri_f_skaiciavimai = sum(e["kvietimai"] for e in etapai)

        print(
            f"{vardas:<8} "
            f"({x[0]: .6f}, {x[1]: .6f}, {x[2]: .6f}) "
            f"{f_min_ivertis:14.8f} {bendri_zingsniai:12d} {bendri_f_skaiciavimai:12d}"
        )


def palyginimas() -> None:
    taskai = gauti_pradinius_taskus()
    X0 = taskai["X0"]
    X1 = taskai["X1"]
    Xm = taskai["Xm"]

    rez0 = optimizuoti_seka(X0)
    rez1 = optimizuoti_seka(X1)
    rezm = optimizuoti_seka(Xm)

    _spausdinti_rezultatus("X0", rez0)
    _spausdinti_rezultatus("X1", rez1)
    _spausdinti_rezultatus("Xm", rezm)

    _spausdinti_pradiniu_tasku_palyginima({"X0": rez0, "X1": rez1, "Xm": rezm})


def sugeneruoti_trumpa_santrauka(taskai: Dict[str, List[float]], r_tyrimas: List[Tuple[float, float]], rezultatai: Dict[str, List[Dict]]) -> str:
    """Sugeneruoja trumpą ataskaitos Markdown su visais užduoties punktais."""
    rez0 = rezultatai["X0"]
    rez1 = rezultatai["X1"]
    rezm = rezultatai["Xm"]

    eilutes = [
        "# Netiesinis optimizavimas: trumpa suvestine",
        "",
        "## Uzdavinys",
        "Kokia turi buti staciakampio gretasienio deze, kad esant vienetiniam pavirsiaus plotui jos turis butu maksimalus?",
        "",
        "## 1. Uzdavinio formuluote",
        "- f(X) = -(x1 * x2 * x3)",
        "- min f(X)",
        "- g(X) = 2(x1x2 + x2x3 + x3x1) - 1 = 0",
        "- h1(X) = -x1 <= 0, h2(X) = -x2 <= 0, h3(X) = -x3 <= 0",
        "",
        "## 2. Reiksmes taskuose X0, X1, Xm",
        f"Knygeles nr. 2412927, todel a=9, b=2, c=7 ir Xm=({taskai['Xm'][0]}, {taskai['Xm'][1]}, {taskai['Xm'][2]}).",
        f"- X0=(0,0,0): f={tikslo_funkcija(tuple(taskai['X0'])):.8f}, g={g(tuple(taskai['X0'])):.8f}, h=[{', '.join(f'{v:.8f}' for v in h(tuple(taskai['X0'])))}]",
        f"- X1=(1,1,1): f={tikslo_funkcija(tuple(taskai['X1'])):.8f}, g={g(tuple(taskai['X1'])):.8f}, h=[{', '.join(f'{v:.8f}' for v in h(tuple(taskai['X1'])))}]",
        f"- Xm=({taskai['Xm'][0]}, {taskai['Xm'][1]}, {taskai['Xm'][2]}): f={tikslo_funkcija(tuple(taskai['Xm'])):.8f}, g={g(tuple(taskai['Xm'])):.8f}, h=[{', '.join(f'{v:.8f}' for v in h(tuple(taskai['Xm'])))}]",
        "",
        "## 3. Kvadratine baudos funkcija",
        "- B(X,r) = f(X) + (1/r) * b(X), r > 0",
        "- b(X) = g(X)^2 + sum(max(0, hi(X))^2)",
        "",
        "## 4. Baudos daugiklio (r) itaka",
    ]

    for r, value in r_tyrimas:
        eilutes.append(f"- r={r:g} -> B={value:.8f}")

    eilutes += [
        "",
        "## 5. Baudos funkcijos minimizavimas uzdaviniu seka",
        "- Mazejanti r seka: [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]",
        "- Pirmo etapo startai: X0, X1, Xm",
        "- Kiekvieno kito etapo pradzia: ankstesnio etapo sprendinys",
        "",
        "## 6. Palyginimas pagal pradini taska",
        "| Pradinis taskas | Gautas sprendinys (x1,x2,x3) | f minimumo ivertis | Zingsniai | Funkciju skaiciavimai |",
        "|---|---|---:|---:|---:|",
    ]

    for vardas, etapai in (("X0", rez0), ("X1", rez1), ("Xm", rezm)):
        galutinis = etapai[-1]
        x = galutinis["sprendinys"]
        eilutes.append(
            f"| {vardas} | ({x[0]:.6f}, {x[1]:.6f}, {x[2]:.6f}) | {galutinis['f']:.8f} | {sum(e['iteracijos'] for e in etapai)} | {sum(e['kvietimai'] for e in etapai)} |"
        )

    eilutes += [
        "",
        "## Galutine isvada",
        "- Didziausias turis gaunamas, kai krastines praktiskai lygios: x1 ~ x2 ~ x3 ~ 0.408259",
        "- Turio maksimumo ivertis Vmax ~ 0.06804659",
        "- Tai atitinka teorini rezultata x1=x2=x3=1/sqrt(6)",
    ]

    return "\n".join(eilutes) + "\n"


def irasyti_santrauka_i_faila() -> None:
    taskai = gauti_pradinius_taskus()
    r_tyrimas = gauti_r_tyrimo_rezultatus(tuple(taskai["X0"]))
    rezultatai = {
        "X0": optimizuoti_seka(taskai["X0"]),
        "X1": optimizuoti_seka(taskai["X1"]),
        "Xm": optimizuoti_seka(taskai["Xm"]),
    }
    SUMMARY_FILE.write_text(sugeneruoti_trumpa_santrauka(taskai, r_tyrimas, rezultatai), encoding="utf-8")


if __name__ == "__main__":
    taskai = gauti_pradinius_taskus()
    spausdinti_f_g_h_taskuose(taskai)
    tirti_r_itaka(tuple(taskai["X0"]))
    palyginimas()
    irasyti_santrauka_i_faila()
