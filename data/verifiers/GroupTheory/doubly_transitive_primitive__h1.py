import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S2 = SymmetricGroup(2)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        # H_1: The action of G on X is doubly transitive
        # In SymPy, this is equivalent to the transitivity degree being at least 2.
        h1 = bool(witness.transitivity_degree >= 2)
    except Exception:
        h1 = False

    try:
        # ¬Q: The action of G on X is not primitive
        # SymPy's is_primitive() returns False for groups of degree <= 2,
        # making S2 a valid counterexample to the dropped hypothesis (degree > 2).
        neg_q = not bool(witness.is_primitive())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The action of G on X is doubly transitive",
    "¬Q: The action of G on X is not primitive"
]

N_HYP = 1
NEG_Q_INDEX = 1