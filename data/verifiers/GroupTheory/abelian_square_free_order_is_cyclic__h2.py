import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import factorint

# Standard group theory objects
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

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
        if h1:
            order = witness.order()
            h1 = (order > 0 and order != sympy.oo)
    except Exception:
        h1 = False

    # H_2: The order of G is a square-free integer
    try:
        if h1:
            order = witness.order()
            factors = factorint(order)
            h2 = all(v == 1 for v in factors.values())
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G is not a cyclic group
    try:
        if h1:
            neg_q = not bool(witness.is_cyclic)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is a square-free integer",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2