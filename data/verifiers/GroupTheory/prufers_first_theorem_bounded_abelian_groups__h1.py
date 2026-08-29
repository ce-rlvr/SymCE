import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            # H_1: There exists a positive integer n such that nx = 0 for all x in G
            # (In multiplicative notation: x^n = e).
            # Every finite permutation group has a bounded exponent (e.g., its order).
            h1 = bool(witness.order() > 0)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            # ¬Q: G is NOT isomorphic to a direct sum of cyclic groups.
            # A direct sum of cyclic groups is necessarily abelian.
            # By the Fundamental Theorem of Finite Abelian Groups, a finite group 
            # is a direct sum of cyclic groups if and only if it is abelian.
            # Therefore, for finite groups, the conclusion fails iff G is non-abelian.
            neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: There exists a positive integer n such that nx = 0 for all x in G",
    "¬Q: G is not isomorphic to a direct sum of cyclic groups"
]

N_HYP = 1
NEG_Q_INDEX = 1