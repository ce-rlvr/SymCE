import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: G is not a nilpotent group
    try:
        if hasattr(witness, 'is_nilpotent'):
            res = witness.is_nilpotent
            if callable(res):
                is_nilp = bool(res())
            else:
                is_nilp = bool(res)
        else:
            # Fallback: compute the lower central series
            series = witness.lower_central_series()
            is_nilp = (series[-1].order() == 1)
            
        neg_q_ok = not is_nilp
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1