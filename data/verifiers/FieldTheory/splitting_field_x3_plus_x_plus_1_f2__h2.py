import sympy
from sympy import Poly
from sympy.abc import x
import math
import functools

def _lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness) -> list[bool]:
    h1 = True
    try:
        p = Poly(witness, x, domain='GF(2)')
        h2 = True
    except Exception:
        h2 = False
        
    try:
        if not h2:
            neg_q = False
        else:
            factors = p.factor_list()
            degrees = [f.degree() for f, m in factors[1]]
            if not degrees:
                deg_E = 1
            else:
                deg_E = functools.reduce(_lcm, degrees, 1)
            neg_q = bool(deg_E != 3)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: F_2 is the finite field with 2 elements", "H_2: E is the splitting field of f(x) over F_2", "not Q: The degree of the extension is not 3"]
N_HYP = 2
NEG_Q_INDEX = 2