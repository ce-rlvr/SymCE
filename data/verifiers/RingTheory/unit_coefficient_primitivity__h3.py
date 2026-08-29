import sympy
from sympy import Poly
from sympy.abc import x, y, z

def conditions(witness):
    try:
        f = Poly(witness) if not isinstance(witness, Poly) else witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(f.domain.is_UFD)
    except Exception:
        h1 = False

    try:
        h2 = bool(not f.is_zero and len(f.gens) == 1)
    except Exception:
        h2 = False

    try:
        c = f.content()
        domain = f.domain
        if hasattr(domain, 'is_unit'):
            is_u = domain.is_unit(c)
        else:
            try:
                domain.exquo(domain.one, c)
                is_u = True
            except Exception:
                is_u = False
        neg_q = not is_u
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial over R",
    "¬Q: The polynomial f is not primitive"
]

N_HYP = 2
NEG_Q_INDEX = 2