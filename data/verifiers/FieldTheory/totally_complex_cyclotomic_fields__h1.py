import sympy
from sympy import cyclotomic_poly
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            h1 = (n >= 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if h1:
            poly = cyclotomic_poly(n, x)
            # The only possible real roots of unity are 1 and -1.
            # Q(zeta_n) has a real embedding iff its minimal polynomial has a real root.
            has_real_root = (poly.subs(x, 1) == 0) or (poly.subs(x, -1) == 0)
            neg_q = bool(has_real_root)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer defining the n-th cyclotomic field",
    "¬Q: Q(zeta_n) has at least one real embedding (is not totally complex)"
]

N_HYP = 1
NEG_Q_INDEX = 1