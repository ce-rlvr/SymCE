import sympy
from sympy import Poly
from sympy.abc import x
import math
from functools import reduce

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        f, g = witness
    except Exception:
        return [False, False, False]
        
    try:
        poly_f = Poly(f, x, domain='ZZ')
        poly_g = Poly(g, x, domain='ZZ')
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if h1_ok:
            coeffs_g = [int(c) for c in poly_g.coeffs()]
            if not coeffs_g:
                h2_ok = False
            else:
                gcd_g = reduce(math.gcd, coeffs_g)
                h2_ok = bool(abs(gcd_g) == 1)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    try:
        if h1_ok:
            poly_fg = poly_f * poly_g
            coeffs_fg = [int(c) for c in poly_fg.coeffs()]
            if not coeffs_fg:
                neg_q_ok = True
            else:
                gcd_fg = reduce(math.gcd, coeffs_fg)
                neg_q_ok = bool(abs(gcd_fg) != 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a UFD and f, g are polynomials over R",
    "H_2: g is a primitive polynomial over R",
    "¬Q: f*g is not a primitive polynomial over R"
]

N_HYP = 2
NEG_Q_INDEX = 2