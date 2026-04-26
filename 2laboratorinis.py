import numpy as np
import math
from dezes_optimizavimas import (
    tikslo_funkcija,
    lygybinis_apribojimas,
    nelygybinis_apribojimas_x,
    nelygybinis_apribojimas_y,
    nelygybinis_apribojimas_z,
    ivertinti_taske,
    kvadratine_baudos_funkcija,
)
from typing import Callable, Tuple, Dict


class OptimizavimoSekosSuBauda:
    """Optimizavimo sekos su mažėjančia baudos parametro r seka."""

    def __init__(self):
        self.iteraciju_skaicius = 0
        self.tikslo_funkcijos_kvietimai = 0
        self.gradiento_kvietimai = 0
        self.sprendinys = None
        self.sekai_sprendiniai = []
        self.sekai_baudos_reiksmes = []
        self.sekai_tikslo_reiksmes = []


def baudos_tikslo_funkcija(x: np.ndarray, baudos_daugiklis: float) -> float:
    """Baudos funkcija perskaičiuota tiesiogiai per numpy."""
    x_lista = tuple(x)
    f_reiksme, g1_reiksme, h1_reiksme, h2_reiksme, h3_reiksme = ivertinti_taske(x_lista)
    bauda = (
        g1_reiksme**2
        + max(0.0, h1_reiksme) ** 2
        + max(0.0, h2_reiksme) ** 2
        + max(0.0, h3_reiksme) ** 2
    )
    return f_reiksme + baudos_daugiklis * bauda


def baudos_gradientas(x: np.ndarray, baudos_daugiklis: float, h: float = 1e-8) -> np.ndarray:
    """Skaitinio gradiento apskaičiavimas."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad[i] = (baudos_tikslo_funkcija(x_plus, baudos_daugiklis) - 
                   baudos_tikslo_funkcija(x_minus, baudos_daugiklis)) / (2 * h)
    return grad


def vienmatis_paieska(
    x_current: np.ndarray,
    kryptis: np.ndarray,
    baudos_daugiklis: float,
    max_iteracijos: int = 50,
) -> Tuple[float, float]:
    """1D minimization su trijų dalių paieška."""
    tol = 1e-6
    a, b = 0.0, 1.0
    
    f_a = baudos_tikslo_funkcija(x_current + a * kryptis, baudos_daugiklis)
    f_b = baudos_tikslo_funkcija(x_current + b * kryptis, baudos_daugiklis)
    
    while f_b < f_a:
        a, b = b, 2 * b
        f_a = f_b
        f_b = baudos_tikslo_funkcija(x_current + b * kryptis, baudos_daugiklis)
    
    c = (a + b) / 2
    for _ in range(max_iteracijos):
        if abs(b - a) < tol:
            break
        c = (a + b) / 2
        f_c = baudos_tikslo_funkcija(x_current + c * kryptis, baudos_daugiklis)
        
        if c - a > b - c:
            test = a + 0.38 * (b - a)
        else:
            test = b - 0.38 * (b - a)
        
        f_test = baudos_tikslo_funkcija(x_current + test * kryptis, baudos_daugiklis)
        
        if f_test < f_c:
            if test < c:
                b = c
            else:
                a = c
        else:
            if test < c:
                a = test
            else:
                b = test
    
    alpha = (a + b) / 2
    return alpha, baudos_tikslo_funkcija(x_current + alpha * kryptis, baudos_daugiklis)


def gradientinis_nusileidimas_sekai(
    x0: np.ndarray,
    baudos_daugiklis: float,
    zingsnio_dydis: float = 0.01,
    max_iteracijos: int = 5000,
    tolerancija: float = 1e-7,
) -> Tuple[np.ndarray, OptimizavimoSekosSuBauda]:
    """Gradientinis nusileidimas su fiksuotu žingsniu."""
    stats = OptimizavimoSekosSuBauda()
    x = x0.copy()
    stats.sekai_sprendiniai.append(x.copy())
    
    for i in range(max_iteracijos):
        stats.iteraciju_skaicius += 1
        
        grad = baudos_gradientas(x, baudos_daugiklis)
        stats.gradiento_kvietimai += 1
        
        grad_norma = np.linalg.norm(grad)
        if grad_norma < tolerancija:
            break
        
        x_nauja = x - zingsnio_dydis * grad
        
        f_val = baudos_tikslo_funkcija(x_nauja, baudos_daugiklis)
        stats.tikslo_funkcijos_kvietimai += 1
        stats.sekai_baudos_reiksmes.append(f_val)
        
        if np.linalg.norm(x_nauja - x) < 1e-15:
            x = x_nauja
            break
        
        x = x_nauja
    
    stats.sprendinys = x
    f_final = baudos_tikslo_funkcija(x, baudos_daugiklis)
    stats.tikslo_funkcijos_kvietimai += 1
    f_be_baudos, _, _, _, _ = ivertinti_taske(tuple(x))
    stats.sekai_tikslo_reiksmes.append(f_be_baudos)
    
    return x, stats


def greiciausiasis_nusileidimas_sekai(
    x0: np.ndarray,
    baudos_daugiklis: float,
    max_iteracijos: int = 5000,
    tolerancija: float = 1e-7,
) -> Tuple[np.ndarray, OptimizavimoSekosSuBauda]:
    """Greičiausiojo nusileidimo metodas su 1D paieška."""
    stats = OptimizavimoSekosSuBauda()
    x = x0.copy()
    stats.sekai_sprendiniai.append(x.copy())
    
    for i in range(max_iteracijos):
        stats.iteraciju_skaicius += 1
        
        grad = baudos_gradientas(x, baudos_daugiklis)
        stats.gradiento_kvietimai += 1
        
        grad_norma = np.linalg.norm(grad)
        if grad_norma < tolerancija:
            break
        
        kryptis = -grad
        alpha, f_val = vienmatis_paieska(x, kryptis, baudos_daugiklis)
        stats.tikslo_funkcijos_kvietimai += 10
        stats.sekai_baudos_reiksmes.append(f_val)
        
        x_nauja = x + alpha * kryptis
        
        if np.linalg.norm(x_nauja - x) < 1e-15:
            x = x_nauja
            break
        
        x = x_nauja
    
    stats.sprendinys = x
    f_be_baudos, _, _, _, _ = ivertinti_taske(tuple(x))
    stats.sekai_tikslo_reiksmes.append(f_be_baudos)
    
    return x, stats


def deformuojamo_simplekso_sekai(
    x0: np.ndarray,
    baudos_daugiklis: float,
    max_iteracijos: int = 10000,
    tolerancija: float = 1e-7,
) -> Tuple[np.ndarray, OptimizavimoSekosSuBauda]:
    """Nelder-Mead simplekso metodas."""
    stats = OptimizavimoSekosSuBauda()
    n = len(x0)
    
    pradinis_zingsnis = 0.1
    simpleksas = [x0.copy()]
    for i in range(n):
        x_i = x0.copy()
        x_i[i] += pradinis_zingsnis
        simpleksas.append(x_i)
    
    stats.sekai_sprendiniai.append(x0.copy())
    
    for iteracija in range(max_iteracijos):
        stats.iteraciju_skaicius += 1
        
        f_reiksmes = np.array([
            baudos_tikslo_funkcija(taskas, baudos_daugiklis) 
            for taskas in simpleksas
        ])
        stats.tikslo_funkcijos_kvietimai += len(simpleksas)
        
        isakizym = np.argsort(f_reiksmes)
        simpleksas = [simpleksas[i] for i in isakizym]
        f_reiksmes = f_reiksmes[isakizym]
        
        virsunes = np.array(simpleksas)
        didziausia_dist = float(np.max(np.linalg.norm(virsunes - virsunes[0], axis=1)))
        
        if didziausia_dist < tolerancija and (f_reiksmes[-1] - f_reiksmes[0]) < tolerancija:
            break
        
        centroidas = np.mean(simpleksas[:-1], axis=0)
        geriausias = simpleksas[0]
        blogiausias = simpleksas[-1]
        
        x_atspindys = centroidas + 1.0 * (centroidas - blogiausias)
        f_atspindys = baudos_tikslo_funkcija(x_atspindys, baudos_daugiklis)
        stats.tikslo_funkcijos_kvietimai += 1
        
        if f_atspindys < f_reiksmes[0]:
            x_prapletimas = centroidas + 2.0 * (x_atspindys - centroidas)
            f_prapletimas = baudos_tikslo_funkcija(x_prapletimas, baudos_daugiklis)
            stats.tikslo_funkcijos_kvietimai += 1
            
            if f_prapletimas < f_atspindys:
                simpleksas[-1] = x_prapletimas
            else:
                simpleksas[-1] = x_atspindys
        elif f_atspindys < f_reiksmes[-2]:
            simpleksas[-1] = x_atspindys
        else:
            if f_atspindys < f_reiksmes[-1]:
                x_traukimas = centroidas + 0.5 * (x_atspindys - centroidas)
            else:
                x_traukimas = centroidas + 0.5 * (blogiausias - centroidas)
            
            f_traukimas = baudos_tikslo_funkcija(x_traukimas, baudos_daugiklis)
            stats.tikslo_funkcijos_kvietimai += 1
            
            if f_traukimas < min(f_atspindys, f_reiksmes[-1]):
                simpleksas[-1] = x_traukimas
            else:
                for i in range(1, len(simpleksas)):
                    simpleksas[i] = simpleksas[0] + 0.5 * (simpleksas[i] - simpleksas[0])
        
        geriausio_indeksas = int(np.argmin(np.array([
            baudos_tikslo_funkcija(taskas, baudos_daugiklis) 
            for taskas in simpleksas
        ])))
        stats.sekai_sprendiniai.append(simpleksas[geriausio_indeksas].copy())
        stats.sekai_baudos_reiksmes.append(f_reiksmes[geriausio_indeksas])
    
    f_reiksmes = np.array([
        baudos_tikslo_funkcija(taskas, baudos_daugiklis) 
        for taskas in simpleksas
    ])
    stats.tikslo_funkcijos_kvietimai += len(f_reiksmes)
    
    geriausio_indeksas = int(np.argmin(f_reiksmes))
    stats.sprendinys = simpleksas[geriausio_indeksas]
    
    f_be_baudos, _, _, _, _ = ivertinti_taske(tuple(stats.sprendinys))
    stats.sekai_tikslo_reiksmes.append(f_be_baudos)
    
    return stats.sprendinys, stats


def optimizuoti_baudos_seka(
    x0_pradinis: np.ndarray,
    baudos_seka: list,
    metodo_funkcija: Callable,
    metodo_vardas: str,
    pradinio_tasko_vardas: str,
) -> Dict:
    """Optimizuoja baudos uždavinių seką, kur pradinis taškas kito uždavinio = praeito sprendinis."""
    print(f"\n{'='*80}")
    print(f"METODAS: {metodo_vardas}")
    print(f"PRADINIS TAŠKAS: {pradinio_tasko_vardas}")
    print(f"{'='*80}\n")
    
    rezultatai_seka = []
    x_current = x0_pradinis.copy()
    
    for idx, baudos_daugiklis in enumerate(baudos_seka):
        print(f"  Etapas {idx + 1}/{len(baudos_seka)}: baudos_daugiklis = {baudos_daugiklis}")
        
        x_sprendinys, statistika = metodo_funkcija(
            x_current,
            baudos_daugiklis,
        )
        
        f_tikslo = tikslo_funkcija(tuple(x_sprendinys))
        
        print(f"    Sprendinys: x = {x_sprendinys[0]:.8f}, y = {x_sprendinys[1]:.8f}, z = {x_sprendinys[2]:.8f}")
        print(f"    f(X) be baudos: {f_tikslo:.8f}")
        print(f"    Iteracijos: {statistika.iteraciju_skaicius}")
        print(f"    Tikslo fn. kvietimai: {statistika.tikslo_funkcijos_kvietimai}")
        print(f"    Gradiento kvietimai: {statistika.gradiento_kvietimai}")
        
        rezultatai_seka.append({
            "baudos_daugiklis": baudos_daugiklis,
            "sprendinys": x_sprendinys.copy(),
            "f_tikslo": f_tikslo,
            "iteracijos": statistika.iteraciju_skaicius,
            "tikslo_kvietimai": statistika.tikslo_funkcijos_kvietimai,
            "gradiento_kvietimai": statistika.gradiento_kvietimai,
        })
        
        x_current = x_sprendinys.copy()
    
    return rezultatai_seka


if __name__ == "__main__":
    # Knygėlės nr: 2412927 -> a=9, b=2, c=7
    a, b, c = 9, 2, 7
    
    # Pradiniai taškai
    x0 = np.array([0.0, 0.0, 0.0], dtype=float)
    x1 = np.array([1.0, 1.0, 1.0], dtype=float)
    xm = np.array([a / 10.0, b / 10.0, c / 10.0], dtype=float)
    
    # Baudos daugiklių seka (mažėjanti seka r)
    baudos_seka = [100.0, 10.0, 1.0, 0.1, 0.01]
    
    # Optimizavimo metodai
    metodai = {
        "Gradientinis nusileidimas": gradientinis_nusileidimas_sekai,
        "Greičiausiasis nusileidimas": greiciausiasis_nusileidimas_sekai,
        "Deformuojamas simpleksas": deformuojamo_simplekso_sekai,
    }
    
    pradiniai_taskai = {
        "X0": x0,
        "X1": x1,
        "Xm": xm,
    }
    
    visos_rezultatai = {}
    
    for pradinio_tasko_vartas, x_pradinis in pradiniai_taskai.items():
        visos_rezultatai[pradinio_tasko_vartas] = {}
        
        for metodo_vardas, metodo_func in metodai.items():
            rezultatai_seka = optimizuoti_baudos_seka(
                x_pradinis,
                baudos_seka,
                metodo_func,
                metodo_vardas,
                pradinio_tasko_vartas,
            )
            visos_rezultatai[pradinio_tasko_vartas][metodo_vardas] = rezultatai_seka
    
    print("\n" + "="*80)
    print("SANTRAUKA: GALUTINIAI SPRENDINIAI")
    print("="*80)
    
    for pradinio_tasko_vardas, pradinis_taskas in pradiniai_taskai.items():
        print(f"\n{pradinio_tasko_vardas} = ({pradinis_taskas[0]:.3f}, {pradinis_taskas[1]:.3f}, {pradinis_taskas[2]:.3f})")
        
        for metodo_vardas in metodai.keys():
            rezultatai = visos_rezultatai[pradinio_tasko_vardas][metodo_vardas]
            finalinis_rezultatas = rezultatai[-1]
            
            print(f"\n  {metodo_vardas}:")
            print(f"    Galutinis sprendinys: {finalinis_rezultatas['sprendinys']}")
            print(f"    f(X): {finalinis_rezultatas['f_tikslo']:.8f}")
            print(f"    Bendra iteracijų suma: {sum(r['iteracijos'] for r in rezultatai)}")
            print(f"    Bendra tikslo fn. kvietimų suma: {sum(r['tikslo_kvietimai'] for r in rezultatai)}")
