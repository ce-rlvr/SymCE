import sympy
import sympy.polys
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x

def conditions(witness):
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            F = witness.domain
            h1 = bool(hasattr(F, 'is_Ring') and F.is_Ring and len(witness.symbols) == 1)
        else:
            F = witness
            h1 = bool(hasattr(F, 'is_Ring') and F.is_Ring)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            F = witness.domain
        else:
            F = witness
        neg_q = not bool(getattr(F, 'is_Field', False))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Ring is the polynomial ring over F in one variable",
    "¬Q: Ring is not a Principal Ideal Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1