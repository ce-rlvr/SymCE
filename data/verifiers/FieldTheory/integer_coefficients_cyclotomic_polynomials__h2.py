import sympy
from sympy.abc import x

CONDITION_LABELS = [
    'H_1: n is a positive integer',
    'neg_Q: Phi_n(x) does not have integer coefficients'
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        h1 = bool(n.is_integer and n > 0)
    except Exception:
        h1 = False

    try:
        n_val = int(sympy.sympify(witness))
        poly = sympy.cyclotomic_poly(n_val, x)
        poly_obj = sympy.Poly(poly, x)
        coeffs = poly_obj.all_coeffs()
        is_in_Z_x = all((sympy.sympify(c).is_integer is True) for c in coeffs)
        neg_q = not is_in_Z_x
    except Exception:
        neg_q = False

    return [h1, neg_q]