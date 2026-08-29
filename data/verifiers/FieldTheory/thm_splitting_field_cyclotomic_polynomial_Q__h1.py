import sympy
from sympy import cyclotomic_poly, totient
from sympy.abc import x

def conditions(witness):
    try:
        n = int(witness)
    except Exception:
        return [False, False, False]

    try:
        h1 = (n >= 1)
    except Exception:
        h1 = False

    h2 = h1

    try:
        if not h1:
            neg_q = False
        else:
            Phi_n = cyclotomic_poly(n, x)
            deg_K = sympy.degree(Phi_n, x)
            expected = totient(n)
            neg_q = bool(deg_K != expected)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let Phi_n be the n-th cyclotomic polynomial",
    "H_2: Let K be the splitting field of Phi_n over Q",
    "¬Q: The degree of the field extension is not equal to phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2