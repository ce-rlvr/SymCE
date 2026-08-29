import sympy
from sympy import Poly
import math
from functools import reduce

x = sympy.Symbol('x')

def list_gcd(l):
    if not l:
        return 0
    try:
        return reduce(math.gcd, [int(c) for c in l])
    except Exception:
        return 0

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
            elif len(witness) == 3:
                _, f, g = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        poly_f = Poly(f, x)
        poly_g = Poly(g, x)
        h1_ok = bool(poly_f.domain.is_ZZ and poly_g.domain.is_ZZ)
    except Exception:
        h1_ok = False
        
    try:
        poly_f = Poly(f, x)
        h2_ok = bool(abs(list_gcd(poly_f.coeffs())) == 1)
    except Exception:
        h2_ok = False
        
    try:
        poly_fg = Poly(sympy.expand(f * g), x)
        neg_q_ok = bool(abs(list_gcd(poly_fg.coeffs())) != 1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a UFD and f and g are polynomials over R",
    "H_2: f is a primitive polynomial",
    "¬Q: f times g is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2