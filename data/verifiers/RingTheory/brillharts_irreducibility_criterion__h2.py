import sympy
from sympy import Poly
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: f is a polynomial with integer coefficients",
    "H_2: 0 <= a_i < b for all coefficients a_i",
    "neg_Q: f is not irreducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_poly_var(f):
    if hasattr(f, 'free_symbols') and len(f.free_symbols) == 1:
        return list(f.free_symbols)[0]
    return x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            f, b = witness
        elif isinstance(witness, dict):
            f = witness.get('f', witness.get('poly'))
            b = witness.get('b')
        else:
            f = witness
            b = None
    except Exception:
        return [False, False, False]

    try:
        var = get_poly_var(f)
        poly_f = Poly(f, var)
        h1 = all(c.is_integer for c in poly_f.all_coeffs())
    except Exception:
        h1 = False

    try:
        var = get_poly_var(f)
        poly_f = Poly(f, var)
        coeffs = poly_f.all_coeffs()
        if b is not None:
            h2 = all(0 <= c < b for c in coeffs)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        var = get_poly_var(f)
        poly_f = Poly(f, var)
        if poly_f.degree() < 1:
            neg_q = True
        else:
            factors = sympy.factor_list(f, domain='QQ')[1]
            num_factors = sum(mult for factor, mult in factors if Poly(factor, var).degree() > 0)
            neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]