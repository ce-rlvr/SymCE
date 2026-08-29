import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    """
    Check if the witness satisfies the hypotheses and fails the conclusion.
    Witness is expected to be a tuple: (G, H, K)
    """
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: K is a subgroup of G
    try:
        h3 = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h3 = False

    # H_4: The index of K in G is finite
    try:
        if h1 and h3:
            h4 = (G.order() % K.order() == 0)
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_5: The greatest common divisor of the index of H in G and the index of K in G is 1
    try:
        if h1 and h2 and h3:
            index_H = G.order() // H.order()
            index_K = G.order() // K.order()
            h5 = math.gcd(index_H, index_K) == 1
        else:
            h5 = False
    except Exception:
        h5 = False

    # ¬Q: G != HK
    try:
        if h1 and h2 and h3:
            try:
                H_elems = list(H.generate())
            except Exception:
                H_elems = list(H.elements)
                
            try:
                K_elems = list(K.generate())
            except Exception:
                K_elems = list(K.elements)
            
            HK_set = {h * k for h in H_elems for k in K_elems}
            neg_q = len(HK_set) != G.order()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: The index of K in G is finite",
    "H_5: The greatest common divisor of the index of H in G and the index of K in G is 1",
    "¬Q: G != HK"
]

N_HYP = 5
NEG_Q_INDEX = 5