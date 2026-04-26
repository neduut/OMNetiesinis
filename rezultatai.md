# Netiesinis optimizavimas: trumpa suvestine

## Uzdavinys
Kokia turi buti staciakampio gretasienio deze, kad esant vienetiniam pavirsiaus plotui jos turis butu maksimalus?

## 1. Uzdavinio formuluote
- f(X) = -(x1 * x2 * x3)
- min f(X)
- g(X) = 2(x1x2 + x2x3 + x3x1) - 1 = 0
- h1(X) = -x1 <= 0, h2(X) = -x2 <= 0, h3(X) = -x3 <= 0

## 2. Reiksmes taskuose X0, X1, Xm
Knygeles nr. 2412927, todel a=9, b=2, c=7 ir Xm=(0.9, 0.2, 0.7).
- X0=(0,0,0): f=-0.00000000, g=-1.00000000, h=[-0.00000000, -0.00000000, -0.00000000]
- X1=(1,1,1): f=-1.00000000, g=5.00000000, h=[-1.00000000, -1.00000000, -1.00000000]
- Xm=(0.9, 0.2, 0.7): f=-0.12600000, g=0.90000000, h=[-0.90000000, -0.20000000, -0.70000000]

## 3. Kvadratine baudos funkcija
- B(X,r) = f(X) + (1/r) * b(X), r > 0
- b(X) = g(X)^2 + sum(max(0, hi(X))^2)

## 4. Baudos daugiklio (r) itaka
- r=1 -> B=1.00000000
- r=0.3 -> B=3.33333333
- r=0.1 -> B=10.00000000
- r=0.03 -> B=33.33333333
- r=0.01 -> B=100.00000000
- r=0.003 -> B=333.33333333
- r=0.001 -> B=1000.00000000

## 5. Baudos funkcijos minimizavimas uzdaviniu seka
- Mazejanti r seka: [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]
- Pirmo etapo startai: X0, X1, Xm
- Kiekvieno kito etapo pradzia: ankstesnio etapo sprendinys

## 6. Palyginimas pagal pradini taska
| Pradinis taskas | Gautas sprendinys (x1,x2,x3) | f minimumo ivertis | Zingsniai | Funkciju skaiciavimai |
|---|---|---:|---:|---:|
| X0 | (0.408259, 0.408259, 0.408259) | -0.06804659 | 718 | 4150 |
| X1 | (0.408259, 0.408259, 0.408259) | -0.06804659 | 735 | 4248 |
| Xm | (0.408259, 0.408259, 0.408259) | -0.06804659 | 715 | 4139 |

## Galutine isvada
- Didziausias turis gaunamas, kai krastines praktiskai lygios: x1 ~ x2 ~ x3 ~ 0.408259
- Turio maksimumo ivertis Vmax ~ 0.06804659
- Tai atitinka teorini rezultata x1=x2=x3=1/sqrt(6)
