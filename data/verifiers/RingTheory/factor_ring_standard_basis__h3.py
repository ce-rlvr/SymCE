import sympy
from sympy import Poly, Symbol, QQ

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, p, n = witness
            elif len(witness) == 2:
                p, n = witness
                F = p.domain
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(getattr(F, 'is_Field', False) or F == QQ)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(p, Poly))
    except Exception:
        h2_ok = False

    try:
        if p.is_zero:
            neg_q_ok = True
        else:
            neg_q_ok = bool(n != p.degree())
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is a polynomial over F",
    "not Q: 1, x, ..., x**(n-1) do not form a basis"
]

N_HYP = 2
NEG_Q_INDEX = 2