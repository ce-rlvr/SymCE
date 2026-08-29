import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() >= 1
    except Exception:
        h1 = False

    try:
        h2 = witness.order() >= 2
    except Exception:
        h2 = False

    try:
        is_elem_abelian = False
        if getattr(witness, 'is_abelian', False):
            order = witness.order()
            factors = factorint(order)
            if len(factors) == 1:
                p = list(factors.keys())[0]
                if all(g.order() in (1, p) for g in witness.generators):
                    is_elem_abelian = True
        neg_q = not is_elem_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G contains at least two elements",
    "¬Q: G is not an elementary abelian p-group for some prime p"
]

N_HYP = 2
NEG_Q_INDEX = 2