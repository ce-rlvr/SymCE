import sympy
from sympy import Poly, gcd

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        a, f = witness
    except Exception:
        return [False, False, False]
    
    try:
        a_sym = sympy.sympify(a)
        f_sym = sympy.sympify(f)
        
        if a_sym.is_integer != True:
            h1_ok = False
        elif not f_sym.free_symbols.issubset({x}):
            h1_ok = False
        else:
            p = Poly(f_sym, x)
            h1_ok = all((c.is_integer == True) for c in p.coeffs())
    except Exception:
        h1_ok = False

    try:
        h2_ok = (a_sym != 0) and (a_sym not in [1, -1])
    except Exception:
        h2_ok = False

    try:
        g = gcd(f_sym, a_sym)
        neg_q_ok = (g not in [1, -1])
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a in R is a non-zero, non-unit element",
    "¬Q: The greatest common divisor of f and a is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2