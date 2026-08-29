import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    # H_1: G is a permutation group acting on a finite set Omega
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The stabilizer G_alpha is trivial for all alpha in Omega
    try:
        if h1:
            # In SymPy, the set Omega is {0, 1, ..., degree - 1}
            # A trivial stabilizer has order 1.
            h2 = all(witness.stabilizer(i).order() == 1 for i in range(witness.degree))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The order of the group G is NOT exactly equal to the cardinality of the set Omega
    try:
        if h1:
            neg_q = witness.order() != witness.degree
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting on a finite set",
    "H_2: The stabilizer of every point is trivial",
    "¬Q: The order of G is not equal to the cardinality of the set"
]

N_HYP = 2
NEG_Q_INDEX = 2