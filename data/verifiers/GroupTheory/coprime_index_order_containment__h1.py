import math
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def is_subgroup(H, G):
    try:
        return bool(H.is_subgroup(G))
    except Exception:
        pass
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(N, G):
    try:
        return bool(G.is_normal(N))
    except Exception:
        pass
    if not is_subgroup(N, G):
        return False
    try:
        for g in G.generators:
            for n in N.generators:
                if (~g * n * g) not in N:
                    return False
                if (g * n * ~g) not in N:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: N is a normal subgroup of G
    h1 = is_normal_subgroup(N, G)
    
    # H_2: H is a subgroup of G
    h2 = is_subgroup(H, G)
    
    # H_3: The greatest common divisor of the order of H and the index of N in G is 1
    try:
        order_H = int(H.order())
        order_G = int(G.order())
        order_N = int(N.order())
        if order_G % order_N != 0:
            h3 = False
        else:
            index_N = order_G // order_N
            h3 = bool(math.gcd(order_H, index_N) == 1)
    except Exception:
        h3 = False
        
    # ¬Q: H is not a subgroup of N
    try:
        neg_q = not is_subgroup(H, N)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: The greatest common divisor of the order of H and the index of N in G is 1",
    "¬Q: H is not a subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3