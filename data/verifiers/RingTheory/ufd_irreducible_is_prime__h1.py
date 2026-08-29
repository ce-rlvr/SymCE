import math
import sympy
from sympy import Rational, Integer

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        d = witness['d']
        p_a, p_b = witness['p']
        x_a, x_b = witness['x']
        y_a, y_b = witness['y']

        if d >= 0:
            return [False, False]

        def norm(a, b):
            return a**2 - d * b**2

        def mult(a1, b1, a2, b2):
            return (a1*a2 + d*b1*b2, a1*b2 + b1*a2)

        def divides(p_a, p_b, x_a, x_b):
            n = norm(p_a, p_b)
            if n == 0: return False
            r = x_a * p_a - d * x_b * p_b
            i = x_b * p_a - x_a * p_b
            return r % n == 0 and i % n == 0

        def has_norm(n):
            if n < 0: return False
            if n == 0: return True
            max_v = int(math.isqrt(n // -d))
            for v in range(-max_v - 2, max_v + 3):
                rem = n + d * v**2
                if rem >= 0 and math.isqrt(rem)**2 == rem:
                    return True
            return False

        def is_irreducible(a, b):
            n = norm(a, b)
            if n <= 1: return False
            for i in range(2, int(math.isqrt(n)) + 1):
                if n % i == 0:
                    if has_norm(i) and has_norm(n // i):
                        return False
            return True

        h1 = is_irreducible(p_a, p_b)

        xy_a, xy_b = mult(x_a, x_b, y_a, y_b)
        div_xy = divides(p_a, p_b, xy_a, xy_b)
        div_x = divides(p_a, p_b, x_a, x_b)
        div_y = divides(p_a, p_b, y_a, y_b)

        neg_q = div_xy and not div_x and not div_y

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: p is an irreducible element in R",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1