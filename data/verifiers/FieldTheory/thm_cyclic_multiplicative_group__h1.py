import sympy
from sympy import QQ, ZZ, RR, CC, S

def conditions(witness) -> list[bool]:
    try:
        neg_q = False
        if witness in (QQ, RR, CC, S.Rationals, S.Reals, S.Complexes):
            neg_q = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            if not getattr(witness, 'is_FiniteField', False):
                neg_q = True
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The multiplicative group of non-zero elements of F is not cyclic"
]

N_HYP = 0
NEG_Q_INDEX = 0