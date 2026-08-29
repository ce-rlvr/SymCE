import sympy
from sympy.combinatorics import PermutationGroup
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        # H_1: G is a finite abelian group
        h1 = isinstance(G, PermutationGroup) and G.is_abelian
    except Exception:
        h1 = False

    try:
        # ¬Q: G does not contain any element of order p
        if not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            neg_q = True
            for elem in G.elements:
                if elem.order() == p:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "¬Q: G does not contain any element of order p"
]

N_HYP = 1
NEG_Q_INDEX = 1