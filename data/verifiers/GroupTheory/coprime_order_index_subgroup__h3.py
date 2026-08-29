import math
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        if isinstance(N, PermutationGroup) and N.is_subgroup(G):
            h2 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * (~g)) not in N:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of the order of H and the index of N in G is 1
    try:
        if hasattr(H, 'order'):
            order_H = H.order() if callable(H.order) else H.order
        else:
            order_H = len(H)
            
        index_G_N = G.order() // N.order()
        h3 = math.gcd(order_H, index_G_N) == 1
    except Exception:
        h3 = False

    # neg_Q: H is not a subset of N
    try:
        if hasattr(H, 'generators'):
            elements_to_check = H.generators
        else:
            elements_to_check = H
            
        neg_q = False
        for h in elements_to_check:
            if h not in N:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: gcd of order of H and index of N in G is 1",
    "neg_Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3