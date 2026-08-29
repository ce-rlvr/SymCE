import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if hasattr(witness, 'is_nilpotent') and witness.is_nilpotent is not None:
            if callable(witness.is_nilpotent):
                h1 = bool(witness.is_nilpotent())
            else:
                h1 = bool(witness.is_nilpotent)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        is_cyclic = False
        if hasattr(witness, 'is_cyclic') and witness.is_cyclic is not None:
            if callable(witness.is_cyclic):
                is_cyclic = bool(witness.is_cyclic())
            else:
                is_cyclic = bool(witness.is_cyclic)
        else:
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
            
            for g in witness.elements:
                if callable(g.order):
                    g_order = g.order()
                else:
                    g_order = g.order
                if g_order == order:
                    is_cyclic = True
                    break
        neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1