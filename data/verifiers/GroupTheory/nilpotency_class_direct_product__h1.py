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
        G, H = witness
        h1 = bool(H.is_nilpotent)
    except Exception:
        h1 = False

    try:
        G, H = witness
        GH = G * H
        if not GH.is_nilpotent:
            neg_q = True
        else:
            cG = G.nilpotency_class
            cH = H.nilpotency_class
            cGH = GH.nilpotency_class
            neg_q = not (cGH == max(cG, cH))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a nilpotent group",
    "¬Q: G × H is not nilpotent or its nilpotency class is not max(c(G), c(H))"
]

N_HYP = 1
NEG_Q_INDEX = 1