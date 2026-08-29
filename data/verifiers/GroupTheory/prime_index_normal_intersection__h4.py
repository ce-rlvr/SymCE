import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        G, N, p, H = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = isprime(p)
    except Exception:
        h3 = False

    # H_4: H is a subgroup of G
    try:
        h4 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h4 = False

    # not Q: H is not a subset of N and index of H cap N in H != p
    try:
        h_in_n = True
        for g in H.generators:
            if g not in N:
                h_in_n = False
                break
        
        # By the Second Isomorphism Theorem, since N is normal in G, 
        # HN is a subgroup and index of H cap N in H = index of N in HN = |HN| / |N|
        HN = PermutationGroup(list(H.generators) + list(N.generators))
        index = HN.order() // N.order()
        
        neg_q = (not h_in_n) and (index != p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "H_4: H is a subgroup of G",
    "not Q: H is not a subset of N and index of H cap N in H != p"
]

N_HYP = 4
NEG_Q_INDEX = 4