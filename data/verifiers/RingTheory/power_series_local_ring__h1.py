import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC, GF
from sympy.abc import X
from sympy.ntheory import factorint

Z = ZZ
Q = QQ

def conditions(witness):
    try:
        h1 = hasattr(witness, 'is_ring') and bool(witness.is_ring)
    except Exception:
        h1 = False

    try:
        if getattr(witness, 'is_Field', False) or getattr(witness, 'is_field', False):
            is_local = True
        elif witness in (ZZ, sympy.S.Integers):
            is_local = False
        elif witness in (QQ, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            is_local = True
        elif hasattr(witness, 'mod'):
            is_local = len(factorint(witness.mod)) == 1
        elif hasattr(witness, 'symbols') and hasattr(witness, 'domain'):
            is_local = False
        else:
            is_local = False
            
        neg_q = not is_local
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is an indeterminate",
    "not Q: The formal power series ring is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1