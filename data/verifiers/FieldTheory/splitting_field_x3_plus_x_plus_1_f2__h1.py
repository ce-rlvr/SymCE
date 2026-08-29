import sympy
from sympy import Poly, Symbol, GF
import math

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: f(x) = x^3 + x + 1 in F_2(x)",
    "H_2: E is the splitting field of f(x) over F_2",
    "neg_Q: The degree of the extension E over F_2 is not 3, or E is not isomorphic to F_8"
]

N_HYP = 2
NEG_Q_INDEX = 2

def _lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, E = witness
        else:
            f = Poly(x**3 + x + 1, x, domain=GF(2))
            E = witness
    except Exception:
        f = None
        E = None

    try:
        expected_f = Poly(x**3 + x + 1, x, domain=GF(2))
        if isinstance(f, Poly):
            h1 = bool(f == expected_f)
        else:
            h1 = bool(Poly(f, x, domain=GF(2)) == expected_f)
    except Exception:
        h1 = False

    try:
        if E is None:
            h2 = False
        else:
            char = getattr(E, 'characteristic', None)
            order = getattr(E, 'order', None)
            if char == 2 and order is not None:
                f_poly = Poly(f, x, domain=GF(2))
                factors = f_poly.factor_list()[1]
                lcm_deg = 1
                for factor, mult in factors:
                    lcm_deg = _lcm(lcm_deg, factor.degree())
                expected_order = 2**lcm_deg
                h2 = bool(order == expected_order)
            else:
                h2 = False
    except Exception:
        h2 = False

    try:
        if E is None:
            q = False
        else:
            char = getattr(E, 'characteristic', None)
            order = getattr(E, 'order', None)
            q = bool(order == 8 and char == 2)
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, neg_q]