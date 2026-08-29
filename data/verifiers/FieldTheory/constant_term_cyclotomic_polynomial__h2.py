import sympy
from sympy.abc import x

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and witness > 1
    except Exception:
        h1 = False

    try:
        poly = sympy.cyclotomic_poly(int(witness), x)
        val = poly.subs(x, 0)
        neg_q = bool(val != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: The evaluation Phi_n(0) is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1