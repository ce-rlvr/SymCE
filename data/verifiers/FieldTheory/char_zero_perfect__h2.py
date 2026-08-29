import sympy
from sympy.abc import x, y, z, t
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

def conditions(witness):
    try:
        h1 = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            char = getattr(witness, 'characteristic', None)
            if char == 0:
                is_perf = True
            elif getattr(witness, 'is_FiniteField', False):
                is_perf = True
            else:
                # In SymPy, any other field of characteristic p > 0 
                # (such as a FractionField over a finite field) is imperfect.
                is_perf = False
            neg_q = not is_perf
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: F is not a perfect field"
]

N_HYP = 1
NEG_Q_INDEX = 1