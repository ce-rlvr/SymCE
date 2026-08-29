import sympy
from sympy import symbols, Poly, sqf_list
import math
from functools import reduce

x, y, z, t = symbols('x y z t')

def conditions(witness):
    try:
        n, g = witness
    except Exception:
        return [False, False, False]
        
    try:
        n_val = int(n)
        h1_ok = (n_val == n) and (n_val >= 2)
    except Exception:
        h1_ok = False
        
    try:
        if not isinstance(g, sympy.Expr):
            g = sympy.sympify(g)
        if len(g.free_symbols - {x}) > 0:
            h2_ok = False
        else:
            p = Poly(g, x)
            h2_ok = p.degree() >= 1
    except Exception:
        h2_ok = False
        
    try:
        if not isinstance(g, sympy.Expr):
            g = sympy.sympify(g)
        coeff, factors = sqf_list(g)
        multiplicities = [e for f, e in factors if Poly(f, x).degree() >= 1]
        
        if not multiplicities:
            neg_q_ok = False
        else:
            g_gcd = reduce(math.gcd, multiplicities)
            n_val = int(n)
            neg_q_ok = math.gcd(n_val, g_gcd) > 1
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: g(x) is a non-constant polynomial",
    "¬Q: y^n - g(x) is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2