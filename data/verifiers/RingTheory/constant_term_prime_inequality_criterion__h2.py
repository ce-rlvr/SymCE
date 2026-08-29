import sympy
from sympy import Poly, factor_list, ZZ, sympify
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f_expr, p_val = witness
        else:
            f_expr = witness
            p_val = None
            
        if isinstance(f_expr, str):
            f_expr = sympify(f_expr)
            
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        else:
            sym = x
            
        poly_f = Poly(f_expr, sym)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(poly_f.degree() >= 1 and poly_f.domain == ZZ)
    except Exception:
        h1 = False

    try:
        coeffs = poly_f.all_coeffs()
        if p_val is None:
            p_val = abs(coeffs[-1])
            
        sum_abs_a_i = sum(abs(c) for c in coeffs[:-1])
        h2 = bool(p_val > sum_abs_a_i)
    except Exception:
        h2 = False

    try:
        factors = factor_list(f_expr, domain='QQ')[1]
        num_non_constant_factors = sum(mult for fac, mult in factors if Poly(fac, sym).degree() > 0)
        neg_q = bool(num_non_constant_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Z of degree n >= 1",
    "H_2: p > sum of |a_i|",
    "neg_Q: f is reducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2