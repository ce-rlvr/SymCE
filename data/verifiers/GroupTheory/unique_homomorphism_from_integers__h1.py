import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
    try:
        G, g = witness
    except Exception:
        return [False, False]

    # H_1: g is an element of G
    try:
        if hasattr(G, 'contains'):
            h1 = bool(G.contains(g))
        else:
            h1 = bool(g in G)
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist a unique group homomorphism phi: Z -> G such that phi(1) = g
    try:
        # If G is a valid group, Z is the free group on 1 generator, 
        # so there is always a unique homomorphism mapping 1 to any element g in G.
        if isinstance(G, PermutationGroup):
            if h1:
                neg_q = False
            else:
                neg_q = True
        else:
            # If G is not a group, the concept of a group homomorphism to G is invalid,
            # so no such homomorphism exists.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "¬Q: There does not exist a unique group homomorphism from Z to G mapping 1 to g"
]

N_HYP = 1
NEG_Q_INDEX = 1