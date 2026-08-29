import math
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: The index of H in G is finite",
    "H_5: The greatest common divisor of the index of H and the index of K is 1",
    "¬Q: G != HK"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False] * 6

    # H1: G is a group
    try:
        if hasattr(G, 'is_group'):
            h1 = bool(G.is_group)
        else:
            h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = bool(H.is_subgroup(G))
        else:
            h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: K is a subgroup of G
    try:
        if hasattr(K, 'is_subgroup'):
            h3 = bool(K.is_subgroup(G))
        else:
            h3 = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h3 = False

    # H4: The index of H in G is finite
    try:
        if hasattr(G, 'index'):
            idx_H = G.index(H)
        else:
            idx_H = G.order() // H.order()
        h4 = idx_H != float('inf') and idx_H is not None
    except Exception:
        h4 = False

    # H5: The greatest common divisor of the index of H and the index of K is 1
    try:
        if hasattr(G, 'index'):
            idx_H = G.index(H)
            idx_K = G.index(K)
        else:
            idx_H = G.order() // H.order()
            idx_K = G.order() // K.order()
        h5 = math.gcd(int(idx_H), int(idx_K)) == 1
    except Exception:
        h5 = False

    # ¬Q: G != HK (The conclusion fails)
    try:
        if hasattr(G, 'HK_equals_G'):
            neg_q = not G.HK_equals_G(H, K)
        else:
            HK = set()
            for h in H.generate_elements():
                for k in K.generate_elements():
                    HK.add(h * k)
            neg_q = len(HK) != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]