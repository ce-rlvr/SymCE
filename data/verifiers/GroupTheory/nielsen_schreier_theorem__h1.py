import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        F, H = witness
    except Exception:
        return [False, False]
    
    # H_1: H is a subgroup of F
    try:
        if hasattr(H, 'is_subgroup'):
            h1_ok = bool(H.is_subgroup(F))
        else:
            h1_ok = all(g in F for g in H.generators)
    except Exception:
        h1_ok = False

    # ¬Q: H is not a free group
    try:
        if isinstance(H, FreeGroup):
            is_free = True
        elif hasattr(H, 'order'):
            ord_H = H.order()
            if ord_H == 1:
                is_free = True
            elif ord_H < float('inf'):
                # A non-trivial finite group has torsion, so it cannot be a free group
                is_free = False
            else:
                is_free = True
        else:
            is_free = True
        neg_q_ok = not is_free
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of F",
    "¬Q: H is not a free group"
]

N_HYP = 1
NEG_Q_INDEX = 1