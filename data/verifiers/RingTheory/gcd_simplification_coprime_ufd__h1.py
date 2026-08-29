import sympy
from sympy import I, sqrt, Rational, Integer, Poly, Symbol
from sympy.abc import x, y, z

# Top-level setup for witness expressions
# (Standard symbols and imaginary unit provided for algebraic numbers)

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero elements of R",
    "H_2: gcd(a, b) = 1 up to units",
    "¬Q: gcd(a, bc) and gcd(a, c) are not associates in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_gcd(u, v):
    try:
        return sympy.gcd(sympy.expand(u), sympy.expand(v))
    except Exception:
        return u.gcd(v)

def check_associates(u, v):
    if hasattr(u, 'is_associate'):
        try:
            return bool(u.is_associate(v))
        except Exception:
            pass
    if u == 0 and v == 0:
        return True
    if u == 0 or v == 0:
        return False
    try:
        ratio = sympy.simplify(u / v)
        if ratio == 1 or ratio == -1:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]
        
    # H1: a, b, c are non-zero elements of R
    try:
        h1 = (a != 0) and (b != 0) and (c != 0)
    except Exception:
        h1 = False
        
    # H2: gcd(a, b) = 1 up to units
    try:
        g_ab = get_gcd(a, b)
        if hasattr(g_ab, 'is_unit'):
            h2 = bool(g_ab.is_unit())
        else:
            h2 = (g_ab == 1 or g_ab == -1)
    except Exception:
        h2 = False
        
    # ¬Q: gcd(a, bc) and gcd(a, c) are not associates in R
    try:
        g_abc = get_gcd(a, b * c)
        g_ac = get_gcd(a, c)
        are_assoc = check_associates(g_abc, g_ac)
        neg_q = not are_assoc
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]