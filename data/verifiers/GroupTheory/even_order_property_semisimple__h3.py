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
        h2 = False
        if h1:
            is_semi = True
            for H in witness.normal_subgroups():
                order = H.order() if callable(H.order) else H.order
                is_ab = H.is_abelian() if callable(H.is_abelian) else H.is_abelian
                if order > 1 and is_ab:
                    is_semi = False
                    break
            h2 = is_semi
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            order = witness.order() if callable(witness.order) else witness.order
            neg_q = (order % 2 != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "¬Q: The order of G is not an even integer"
]

N_HYP = 2
NEG_Q_INDEX = 2