import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False] * 6
        G, H, K = witness
    except Exception:
        return [False] * 6

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # H_3: The index (G:H) is finite
    try:
        h3 = h2 and (G.order() % H.order() == 0)
    except Exception:
        h3 = False

    # H_4: The index (G:K) is finite
    try:
        if isinstance(K, PermutationGroup):
            k_order = K.order()
            k_in_g = all(g in G for g in K.generators)
        else:
            K_set = set(K)
            k_order = len(K_set)
            k_in_g = all(g in G for g in K_set)
        
        h4 = k_in_g and k_order > 0 and (G.order() % k_order == 0)
    except Exception:
        h4 = False

    # H_5: The greatest common divisor of (G:H) and (G:K) is 1
    try:
        if h3 and h4:
            idx_H = G.order() // H.order()
            idx_K = G.order() // k_order
            h5 = math.gcd(idx_H, idx_K) == 1
        else:
            h5 = False
    except Exception:
        h5 = False

    # ¬Q: G != HK
    try:
        if h1 and h2 and h4:
            H_elems = set(H.generate())
            if isinstance(K, PermutationGroup):
                K_elems = set(K.generate())
            else:
                K_elems = set(K)
            
            HK_elems = {h * k for h in H_elems for k in K_elems}
            G_elems = set(G.generate())
            neg_q = HK_elems != G_elems
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index (G:H) is finite",
    "H_4: The index (G:K) is finite",
    "H_5: The greatest common divisor of (G:H) and (G:K) is 1",
    "¬Q: G != HK"
]

N_HYP = 5
NEG_Q_INDEX = 5