import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is an abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H_2: The order of G is a square-free integer
    try:
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
            
        if order <= 0:
            h2 = False
        else:
            factors = factorint(order)
            h2 = all(v == 1 for v in factors.values())
    except Exception:
        h2 = False

    # ¬Q: G is not a cyclic group
    try:
        if hasattr(witness, 'is_cyclic'):
            is_cyc = witness.is_cyclic
        else:
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
            is_cyc = any(g.order() == order for g in witness.elements)
        neg_q = not bool(is_cyc)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: The order of G is a square-free integer",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2