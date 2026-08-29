import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness) -> list[bool]:
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and int(G.order()) > 0
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = hasattr(H, 'generators') and all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of the order of H and the index of N in G is 1
    try:
        n_is_subgroup = hasattr(N, 'generators') and all(g in G for g in N.generators)
        if n_is_subgroup and int(G.order()) % int(N.order()) == 0:
            index = int(G.order()) // int(N.order())
            h3 = math.gcd(int(H.order()), index) == 1
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: H is not a subgroup of N
    try:
        neg_q = not all(g in N for g in H.generators)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: The greatest common divisor of the order of H and the index of N in G is 1",
    "¬Q: H is not a subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3