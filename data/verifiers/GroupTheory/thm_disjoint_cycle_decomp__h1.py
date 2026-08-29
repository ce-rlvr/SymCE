import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # H_1: Let \pi be an element of S_n
    try:
        H_1_ok = isinstance(witness, Permutation)
    except Exception:
        H_1_ok = False

    # ¬Q: \pi cannot be uniquely expressed as a product of disjoint cycles
    try:
        if not H_1_ok:
            neg_Q_ok = False
        else:
            # The dropped hypothesis from the true theorem is that \pi is not the identity.
            # The identity permutation cannot be uniquely expressed as a product of disjoint cycles
            # (either it requires an empty product which is not a valid product of cycles, 
            # or it can be expressed using arbitrary 1-cycles like (1) or (2), which is not unique).
            # For any non-identity permutation, the decomposition into disjoint cycles of length >= 2 is unique.
            neg_Q_ok = bool(witness.is_Identity)
    except Exception:
        neg_Q_ok = False

    return [H_1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: pi is an element of S_n",
    "¬Q: pi cannot be uniquely expressed as a product of disjoint cycles"
]

N_HYP = 1
NEG_Q_INDEX = 1