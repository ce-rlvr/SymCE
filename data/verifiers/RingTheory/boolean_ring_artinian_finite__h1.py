import sympy
from sympy import QQ, ZZ, RR, CC

def _is_finite_ring(R):
    if R in [QQ, ZZ, RR, CC]:
        return False
    cls_name = R.__class__.__name__
    if 'Finite' in cls_name or 'Galois' in cls_name or 'Mod' in cls_name:
        return True
    if getattr(R, 'is_finite', False):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        # H_1: R is an Artinian ring
        # Fields and finite rings are Artinian.
        is_art = False
        if getattr(witness, 'is_Field', False) or witness in [QQ, RR, CC]:
            is_art = True
        elif _is_finite_ring(witness):
            is_art = True
        h1_ok = bool(is_art)
    except Exception:
        h1_ok = False

    try:
        # ¬Q: R is not a finite ring
        neg_q_ok = not _is_finite_ring(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1