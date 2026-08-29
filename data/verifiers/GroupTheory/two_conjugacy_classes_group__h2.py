import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: G is not isomorphic to the cyclic group of order 2
    try:
        # A finite group is isomorphic to Z2 if and only if its order is exactly 2
        neg_q = witness.order() != 2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not isomorphic to the cyclic group of order 2"
]

N_HYP = 1
NEG_Q_INDEX = 1