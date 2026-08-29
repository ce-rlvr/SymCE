import sympy
from sympy import Poly, Symbol, im

x = Symbol('x')

def conditions(witness):
    try:
        p = Poly(witness, x)
        h1 = all((c.is_real == True) for c in p.coeffs())
    except Exception:
        h1 = False

    h2 = h1

    try:
        p = Poly(witness, x)
        deg = p.degree()
        rts = p.nroots()
        has_complex_root = any(float(abs(im(r))) > 1e-9 for r in rts)
        neg_q = not (deg == 2 and has_complex_root)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let R be a real closed field (assumed R=Reals)",
    "H_2: Let E be the splitting field of f(x) over R (f(x) is a real polynomial)",
    "¬Q: The degree of f(x) is not 2, or E is not isomorphic to R(sqrt(-1))"
]

N_HYP = 2
NEG_Q_INDEX = 2