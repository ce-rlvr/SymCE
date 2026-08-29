import sympy
from sympy import Symbol, Poly

x = Symbol('x')

def conditions(witness):
    try:
        h1 = (type(witness) is int or isinstance(witness, sympy.Integer)) and witness > 0 and witness < 105
    except Exception:
        h1 = False

    try:
        if (type(witness) is int or isinstance(witness, sympy.Integer)) and witness > 0:
            n = int(witness)
            poly_expr = sympy.cyclotomic_poly(n, x)
            coeffs = Poly(poly_expr, x).all_coeffs()
            neg_q = not all(c in [-1, 0, 1] for c in coeffs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer strictly less than 105",
    "¬Q: Some coefficient of Phi_n(x) is not in {-1, 0, 1}"
]

N_HYP = 1
NEG_Q_INDEX = 1