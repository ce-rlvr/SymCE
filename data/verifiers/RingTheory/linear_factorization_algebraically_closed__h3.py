import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple):
        f = witness[-1]
    else:
        f = witness

    # H_1: K is an algebraically closed field
    try:
        h1 = True
    except Exception:
        h1 = False

    # H_2: f is a polynomial
    try:
        p = Poly(f, x)
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: f cannot be factored
    try:
        p = Poly(f, x)
        # Over an algebraically closed field, every non-zero polynomial can be factored.
        # The zero polynomial cannot be factored into the form c(x-a_1)...(x-a_n) with c != 0.
        neg_q = bool(p.is_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f is a polynomial",
    "¬Q: f cannot be factored"
]

N_HYP = 2
NEG_Q_INDEX = 2