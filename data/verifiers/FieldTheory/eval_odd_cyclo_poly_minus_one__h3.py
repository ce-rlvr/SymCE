import sympy
from sympy.abc import x

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and witness >= 3
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, (int, sympy.Integer)) and witness % 2 != 0
    except Exception:
        h2 = False

    try:
        if not isinstance(witness, (int, sympy.Integer)) or witness < 1:
            neg_q = False
        else:
            n = int(witness)
            poly = sympy.cyclotomic_poly(n, x)
            val = poly.subs(x, -1)
            neg_q = bool(val != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: n is an odd number",
    "¬Q: Phi_n(-1) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2