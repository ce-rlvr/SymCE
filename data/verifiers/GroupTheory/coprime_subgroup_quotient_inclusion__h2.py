import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
        G, H, N = witness
    except Exception:
        return [False, False, False, False]

    try:
        order = G.order()
        h1 = isinstance(order, (int, sympy.Integer)) and order > 0
    except Exception:
        h1 = False

    try:
        h2 = bool(hasattr(H, 'is_subgroup') and H.is_subgroup(G))
    except Exception:
        h2 = False

    try:
        is_N_subgroup = hasattr(N, 'is_subgroup') and N.is_subgroup(G)
        if is_N_subgroup:
            index = G.order() // N.order()
            h3 = bool(math.gcd(int(H.order()), int(index)) == 1)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        is_subset = all(g in N for g in H.generators)
        neg_q = not is_subset
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: gcd(|H|, index of N in G) = 1",
    "¬Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3