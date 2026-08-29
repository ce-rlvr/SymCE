import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of the index of H in G and the index of K in G is 1
    try:
        if not (isinstance(K, PermutationGroup) and K.is_subgroup(G)):
            h3 = False
        else:
            size_G = int(G.order())
            size_H = int(H.order())
            size_K = int(K.order())
            
            if size_H == 0 or size_K == 0 or size_G % size_H != 0 or size_G % size_K != 0:
                h3 = False
            else:
                idx_H = size_G // size_H
                idx_K = size_G // size_K
                h3 = math.gcd(idx_H, idx_K) == 1
    except Exception:
        h3 = False

    # neg_Q: The index of H intersection K in G is not equal to the product of their indices
    try:
        elems_H = set(H.generate())
        elems_K = set(K.generate())
            
        intersection = elems_H.intersection(elems_K)
        size_int = int(len(intersection))
        
        size_G = int(G.order())
        size_H = int(H.order())
        size_K = int(K.order())
            
        idx_H = size_G // size_H
        idx_K = size_G // size_K
        
        if size_int == 0:
            neg_q = True
        elif size_G % size_int != 0:
            neg_q = True
        else:
            idx_int = size_G // size_int
            neg_q = idx_int != (idx_H * idx_K)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: The greatest common divisor of the index of H in G and the index of K in G is 1",
    "¬Q: The index of H intersection K in G is not equal to the product of their indices"
]

N_HYP = 3
NEG_Q_INDEX = 3