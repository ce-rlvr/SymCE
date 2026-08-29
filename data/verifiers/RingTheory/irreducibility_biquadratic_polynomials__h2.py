import sympy
from sympy import Symbol, Poly, QQ, GF, Rational, Integer

x = Symbol('x')

def is_square(val, K):
    try:
        if val == 0:
            return True
        p = Poly(x**2 - val, x, domain=K)
        return not p.is_irreducible
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        K, a, b = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = bool(K.is_Field and K.characteristic != 2)
    except Exception:
        h1 = False

    try:
        h2 = not is_square(b, K)
    except Exception:
        h2 = False

    try:
        h3 = not is_square(a**2 - 4*b, K)
    except Exception:
        h3 = False

    try:
        h4 = not is_square(b*(a**2 - 4*b), K)
    except Exception:
        h4 = False

    try:
        p = Poly(x**4 + a*x**2 + b, x, domain=K)
        neg_q = not p.is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: b is not a square in K",
    "H_3: a^2 - 4b is not a square in K",
    "H_4: b(a^2 - 4b) is not a square in K",
    "¬Q: x^4 + a x^2 + b is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4