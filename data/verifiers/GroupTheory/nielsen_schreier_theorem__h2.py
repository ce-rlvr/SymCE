import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup,
    free_group
)

# Top-level setup
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

F1 = free_group('x')[0]
F2 = free_group('a, b')[0]
FreeGroupClass = type(F1)

def conditions(witness) -> list[bool]:
    F, H = None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, H = witness
        elif hasattr(witness, 'F') and hasattr(witness, 'H'):
            F, H = witness.F, witness.H
        elif isinstance(witness, dict) and 'F' in witness and 'H' in witness:
            F, H = witness['F'], witness['H']
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: F is a free group
    try:
        if isinstance(F, FreeGroupClass):
            h1 = True
        elif hasattr(F, 'order'):
            try:
                if F.order() == 1:
                    h1 = True
                else:
                    h1 = False
            except Exception:
                h1 = False
        elif hasattr(F, 'relators') and len(F.relators) == 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: H is NOT a free group
    try:
        if isinstance(H, FreeGroupClass):
            is_free = True
        elif hasattr(H, 'relators') and len(H.relators) == 0:
            is_free = True
        elif hasattr(H, 'order'):
            try:
                ord_H = H.order()
                if ord_H == 1:
                    is_free = True
                else:
                    is_free = False
            except Exception:
                is_free = False
        else:
            is_free = False
            
        neg_q = not is_free
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: H is not a free group"
]

N_HYP = 1
NEG_Q_INDEX = 1