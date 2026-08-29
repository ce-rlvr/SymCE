import sympy
from sympy.polys.domains import ZZ, QQ, EX

class InfPolyRing:
    is_Noetherian = False
    is_noetherian = False

R_inf = InfPolyRing()

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_Noetherian'):
            neg_q = not bool(witness.is_Noetherian)
        elif hasattr(witness, 'is_noetherian'):
            neg_q = not bool(witness.is_noetherian)
        elif witness == EX:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["not Q: Laurent polynomial ring over R is not Noetherian"]
N_HYP = 0
NEG_Q_INDEX = 0