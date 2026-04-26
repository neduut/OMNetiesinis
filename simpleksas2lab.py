from __future__ import annotations

import math
from typing import Callable, List, Sequence, Tuple

Point = List[float]
Objective = Callable[[Tuple[float, float, float]], float]


def _vector_add(a: Point, b: Point) -> Point:
    return [ai + bi for ai, bi in zip(a, b)]


def _vector_sub(a: Point, b: Point) -> Point:
    return [ai - bi for ai, bi in zip(a, b)]


def _vector_mul(a: Point, scalar: float) -> Point:
    return [scalar * ai for ai in a]


def _norm(a: Point) -> float:
    return math.sqrt(sum(ai * ai for ai in a))


def _centroid(simplex: Sequence[Point]) -> Point:
    n = len(simplex[0])
    m = len(simplex)
    return [sum(p[i] for p in simplex) / m for i in range(n)]


def simpleksas(
    func: Objective,
    start: Sequence[float],
    max_iteracijos: int = 2000,
    tolerancija: float = 1e-6,
    pradinis_zingsnis: float = 0.1,
) -> Tuple[Point, int, int]:
    """Deformuojamo simplekso metodas be jokiu ziniu apie apribojimus ar baudas."""
    x0 = list(start)
    n = len(x0)
    simplex: List[Point] = [x0.copy()]
    kvietimai = 0

    for i in range(n):
        xi = x0.copy()
        xi[i] += pradinis_zingsnis
        simplex.append(xi)

    for iteracija in range(1, max_iteracijos + 1):
        f_values = [func(tuple(p)) for p in simplex]
        kvietimai += len(simplex)

        order = sorted(range(len(f_values)), key=lambda i: f_values[i])
        simplex = [simplex[i] for i in order]
        f_values = [f_values[i] for i in order]

        simplex_size = max(_norm(_vector_sub(p, simplex[0])) for p in simplex)
        if simplex_size < tolerancija and (max(f_values) - min(f_values)) < tolerancija:
            return simplex[0], iteracija, kvietimai

        c = _centroid(simplex[:-1])
        worst = simplex[-1]

        reflection = _vector_add(c, _vector_sub(c, worst))
        f_reflection = func(tuple(reflection))
        kvietimai += 1

        if f_reflection < f_values[0]:
            expansion = _vector_add(c, _vector_mul(_vector_sub(reflection, c), 2.0))
            f_expansion = func(tuple(expansion))
            kvietimai += 1
            simplex[-1] = expansion if f_expansion < f_reflection else reflection
        elif f_reflection < f_values[-2]:
            simplex[-1] = reflection
        else:
            if f_reflection < f_values[-1]:
                contraction = _vector_add(c, _vector_mul(_vector_sub(reflection, c), 0.5))
            else:
                contraction = _vector_add(c, _vector_mul(_vector_sub(worst, c), 0.5))

            f_contraction = func(tuple(contraction))
            kvietimai += 1

            if f_contraction < min(f_reflection, f_values[-1]):
                simplex[-1] = contraction
            else:
                best = simplex[0]
                for i in range(1, len(simplex)):
                    simplex[i] = _vector_add(best, _vector_mul(_vector_sub(simplex[i], best), 0.5))

    f_values = [func(tuple(p)) for p in simplex]
    kvietimai += len(simplex)
    best_idx = min(range(len(f_values)), key=lambda i: f_values[i])
    return simplex[best_idx], max_iteracijos, kvietimai
