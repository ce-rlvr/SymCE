import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # The hypercenter Z_infty(G) is the terminal member of the upper central series.
        # The first member of the series is the center Z(G).
        # Z_infty(G) is trivial if and only if Z(G) is trivial.
        # Therefore, the negated conclusion (Z_infty(G) is NOT trivial) 
        # is equivalent to Z(G) being non-trivial.
        neg_q = witness.center().order() > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Z_\\infty(G) is the hypercenter of G",
    "¬Q: Z_\\infty(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1