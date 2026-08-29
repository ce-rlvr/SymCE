import math
import sympy
from sympy import Poly
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            f = witness[0]
            g = witness[1]
        else:
            return [False, False, False]
            
        poly_f = Poly(f)
        poly_g = Poly(g)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(poly_f.is_irreducible)
    except Exception:
        h1 = False
        
    try:
        deg_f = int(poly_f.degree())
        deg_g = int(poly_g.degree())
        h2 = math.gcd(deg_f, deg_g) == 1
    except Exception:
        h2 = False
        
    try:
        factors_g = sympy.factor_list(poly_g)
        neg_q = len(factors_g[1]) >= 2
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial over F",
    "H_2: gcd(deg(f), dim_F(E)) == 1",
    "¬Q: f is not irreducible over E"
]

N_HYP = 2
NEG_Q_INDEX = 2