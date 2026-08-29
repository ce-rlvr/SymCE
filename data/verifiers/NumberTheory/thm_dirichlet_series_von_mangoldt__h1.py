import sympy as sp
import math

def conditions(witness):
    try:
        s = sp.sympify(witness)
        h1 = bool(s.is_number)
    except Exception:
        h1 = False

    try:
        s = sp.sympify(witness)
        h2 = bool(s.is_number)
    except Exception:
        h2 = False

    try:
        s = sp.sympify(witness)
        if not s.is_number:
            neg_q = False
        else:
            re_s = float(sp.re(s))
            if math.isnan(re_s) or math.isinf(re_s):
                neg_q = False
            else:
                neg_q = bool(re_s <= 1.0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\Lambda(n) is the von Mangoldt function",
    "H_2: \\zeta(s) is the Riemann zeta function",
    "¬Q: The Dirichlet series does not converge absolutely to -\\zeta'(s)/\\zeta(s)"
]

N_HYP = 2
NEG_Q_INDEX = 2