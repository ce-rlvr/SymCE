from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() >= 1
    except Exception:
        h1 = False

    try:
        neg_q = False
        if h1:
            n = witness.order()
            is_cyclic = False
            if witness.is_abelian:
                for g in witness.elements:
                    if g.order() == n:
                        is_cyclic = True
                        break
            if not is_cyclic:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G has a finite order n >= 1",
    "¬Q: G is not isomorphic to the cyclic group of order n"
]

N_HYP = 1
NEG_Q_INDEX = 1