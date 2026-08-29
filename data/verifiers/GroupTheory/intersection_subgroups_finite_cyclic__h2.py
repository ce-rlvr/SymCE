import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, H, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and G.is_abelian
        if h1:
            order = G.order()
            h1 = any(g.order() == order for g in G.elements)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h2 = False

    try:
        h_elems = set(H.elements)
        k_elems = set(K.elements)
        intersection_size = len(h_elems.intersection(k_elems))
        expected_size = math.gcd(H.order(), K.order())
        neg_q = intersection_size != expected_size
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: K is a subgroup of G",
    "¬Q: The order of the intersection H \cap K is not equal to gcd(|H|, |K|)"
]

N_HYP = 2
NEG_Q_INDEX = 2