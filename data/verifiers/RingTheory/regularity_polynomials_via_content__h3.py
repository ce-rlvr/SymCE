import sympy
from sympy import Poly
from sympy.abc import x
from math import gcd
from functools import reduce

# Top-level setup: named object bindings that the witness expression may reference.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, f = witness
        else:
            n = 0
            f = witness
            
        h1 = isinstance(n, int) and n >= 0
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            p = Poly(f, x, domain='ZZ')
            h2 = True
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            p = Poly(f, x, domain='ZZ')
            coeffs = p.all_coeffs()
            if n == 0:
                neg_q = all(c == 0 for c in coeffs)
            elif n == 1:
                neg_q = False
            else:
                c_gcd = reduce(gcd, [int(c) % n for c in coeffs] + [n])
                neg_q = (c_gcd > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial",
    "¬Q: f is not a regular element"
]

N_HYP = 2
NEG_Q_INDEX = 2