import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
        G, N = witness
    except Exception:
        return [False, False]

    try:
        h1 = (N.order() > 1) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h1 = False

    try:
        domain_size = G.degree
        if domain_size == 0:
            neg_q = False
        else:
            orbit_0 = N.orbit(0)
            is_transitive = (len(orbit_0) == domain_size)
            neg_q = not is_transitive
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a non-trivial normal subgroup of G",
    "¬Q: The action of N on X is not transitive"
]

N_HYP = 1
NEG_Q_INDEX = 1