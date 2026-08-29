import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        h1 = False
        if hasattr(witness, 'order') and hasattr(witness, 'generators'):
            order = witness.order()
            if order > 0 and order < float('inf'):
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if hasattr(witness, 'normal_subgroups'):
            normal_subs = witness.normal_subgroups()
            neg_q = (len(normal_subs) == 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is a simple group"
]

N_HYP = 1
NEG_Q_INDEX = 1