import sympy
from sympy import GF, QQ, ZZ, S

# Top-level setup: standard fields and rings
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)
F7 = GF(7)
Q = QQ
Z = ZZ
R = S.Reals
C = S.Complexes

def is_field(w):
    """Check if the witness represents a field."""
    if isinstance(w, int):
        return sympy.isprime(w)
    if hasattr(w, 'is_Field') and w.is_Field:
        return True
    if hasattr(w, 'is_field') and w.is_field:
        return True
    if w in (S.Rationals, S.Reals, S.Complexes, QQ):
        return True
    return False

def is_Z2(w):
    """Check if the witness is isomorphic to the field with two elements."""
    if isinstance(w, int):
        return w == 2
    if hasattr(w, 'order'):
        try:
            if w.order == 2:
                return True
        except Exception:
            pass
    if hasattr(w, 'size'):
        try:
            if w.size == 2:
                return True
        except Exception:
            pass
    try:
        if w == GF(2):
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_field(witness))
    except Exception:
        h1 = False

    try:
        neg_q = not bool(is_Z2(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a field",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1