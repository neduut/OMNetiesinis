import math


def tikslo_funkcija(x):
    """tikslas min problemai: neigiamas tūris."""
    a, b, c = x
    return -(a * b * c)


def lygybinis_apribojimas(x):
    """lygybinis apribojimas: paviršiaus plotas lygus 1"""
    a, b, c = x
    return 2 * (a * b + b * c + c * a) - 1


def nelygybinis_apribojimas_x(x):
    return -x[0]


def nelygybinis_apribojimas_y(x):
    return -x[1]


def nelygybinis_apribojimas_z(x):
    return -x[2]


def ivertinti_taske(x):
    f_reiksme = tikslo_funkcija(x)
    g1_reiksme = lygybinis_apribojimas(x)
    h1_reiksme = nelygybinis_apribojimas_x(x)
    h2_reiksme = nelygybinis_apribojimas_y(x)
    h3_reiksme = nelygybinis_apribojimas_z(x)
    return f_reiksme, g1_reiksme, h1_reiksme, h2_reiksme, h3_reiksme


def spausdinti_tasko_reiksmes(pavadinimas, x):
    f_reiksme, g1_reiksme, h1_reiksme, h2_reiksme, h3_reiksme = ivertinti_taske(x)
    print(f"{pavadinimas} = {x}")
    print(f"  f(X)  = {f_reiksme:.6f}")
    print(f"  g1(X) = {g1_reiksme:.6f}")
    print(f"  h1(X) = {h1_reiksme:.6f}")
    print(f"  h2(X) = {h2_reiksme:.6f}")
    print(f"  h3(X) = {h3_reiksme:.6f}")


def kvadratine_baudos_funkcija(x, baudos_daugiklis):
    """F_b(X)=f(X)+rho*(g1(X)^2+max(0,h1)^2+max(0,h2)^2+max(0,h3)^2)."""
    f_reiksme, g1_reiksme, h1_reiksme, h2_reiksme, h3_reiksme = ivertinti_taske(x)
    bauda = (
        g1_reiksme**2
        + max(0.0, h1_reiksme) ** 2
        + max(0.0, h2_reiksme) ** 2
        + max(0.0, h3_reiksme) ** 2
    )
    return f_reiksme + baudos_daugiklis * bauda

# tiriamos reiksmes su daugikliais 0.1, 1.0, 10.0, 100.0, 1000.0
def baudos_daugiklio_itakos_tyrimas(taskai, daugikliai):
    print("\nBaudos daugiklio itaka F_b(X) reiksmems:")
    for pavadinimas, taskas in taskai:
        print(f"\n{pavadinimas} = {taskas}")
        for baudos_daugiklis in daugikliai:
            fb_reiksme = kvadratine_baudos_funkcija(taskas, baudos_daugiklis)
            print(f"  baudos_daugiklis={baudos_daugiklis:7.2f} -> F_b={fb_reiksme:10.6f}")


if __name__ == "__main__":
    krastine = 1 / math.sqrt(6)
    x, y, z = krastine, krastine, krastine
    turis = 1 / (6 * math.sqrt(6))
    print(f"Optimalūs matmenys: x = {x:.10f}, y = {y:.10f}, z = {z:.10f}")
    print(f"Maksimalus tūris: {turis:.10f}")

    # knygeles nr: 2412927 -> a=9, b=2, c=7
    a, b, c = 9, 2, 7
    x0 = (0.0, 0.0, 0.0)
    x1 = (1.0, 1.0, 1.0)
    xm = (a / 10, b / 10, c / 10)

    print("\nFunkcijų reikšmės taškuose:")
    spausdinti_tasko_reiksmes("X0", x0)
    spausdinti_tasko_reiksmes("X1", x1)
    spausdinti_tasko_reiksmes("Xm", xm)

    baudos_daugiklis = 10.0
    print(f"\nKvadratine baudos funkcija (baudos_daugiklis={baudos_daugiklis:.1f}):")
    print(f"  F_b(X0) = {kvadratine_baudos_funkcija(x0, baudos_daugiklis):.6f}")
    print(f"  F_b(X1) = {kvadratine_baudos_funkcija(x1, baudos_daugiklis):.6f}")
    print(f"  F_b(Xm) = {kvadratine_baudos_funkcija(xm, baudos_daugiklis):.6f}")

    taskai = [("X0", x0), ("X1", x1), ("Xm", xm)]
    daugikliai = [0.1, 1.0, 10.0, 100.0, 1000.0]
    baudos_daugiklio_itakos_tyrimas(taskai, daugikliai)