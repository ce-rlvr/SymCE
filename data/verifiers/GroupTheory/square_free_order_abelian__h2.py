import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))

def conditions(witness):
    try:
        if callable(witness.is_abelian):
            h1 = bool(witness.is_abelian())
        else:
            h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_cyclic'):
            if callable(witness.is_cyclic):
                is_cyclic = bool(witness.is_cyclic())
            else:
                is_cyclic = bool(witness.is_cyclic)
        else:
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
                
            elements = witness.elements() if callable(witness.elements) else witness.elements
            is_cyclic = False
            for g in elements:
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
    "H_1: G is a finite abelian group",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1