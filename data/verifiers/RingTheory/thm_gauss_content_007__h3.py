import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness):
    try:
        a, f = witness
        a_sym = sympy.sympify(a)
        f_sym = sympy.sympify(f)
    except Exception:
        return [False, False, False]

    try:
        poly_f = Poly(f_sym, x)
        h1 = a_sym.is_Integer and all(c.is_Integer for c in poly_f.coeffs())
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f_sym, x)
        h2 = not poly_f.is_zero
    except Exception:
        h2 = False

    try:
        _, prim_af = sympy.primitive(a_sym * f_sym, x)
        _, prim_f = sympy.primitive(f_sym, x)
        
        diff1 = sympy.expand(prim_af - prim_f)
        diff2 = sympy.expand(prim_af + prim_f)
        is_associate = (diff1 == 0) or (diff2 == 0)
        neg_q = not is_associate
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial",
    "not Q: The primitive part of a*f is not associate to the primitive part of f"
]

N_HYP = 2
NEG_Q_INDEX = 2