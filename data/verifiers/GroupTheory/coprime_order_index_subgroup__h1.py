import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False

    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False

    try:
        h3 = False
        order_H = int(H.order())
        order_G = int(G.order())
        order_N = int(N.order())
        if order_G % order_N == 0:
            index_G_N = order_G // order_N
            h3 = (math.gcd(order_H, index_G_N) == 1)
    except Exception:
        h3 = False

    try:
        neg_q = not bool(H.is_subgroup(N))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: The greatest common divisor of the order of H and the index of N in G is 1",
    "¬Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3