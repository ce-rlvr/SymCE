import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(K, PermutationGroup) and all(g in G for g in K.generators)
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            index_GK = G.order() // K.order()
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if not isinstance(H, PermutationGroup) or not h1 or not h2:
            neg_q = False
        else:
            def get_normalized_elements(group):
                els = set()
                for g in group.generate():
                    arr = list(g.array_form)
                    while arr and arr[-1] == len(arr) - 1:
                        arr.pop()
                    els.add(tuple(arr))
                return els

            H_els = get_normalized_elements(H)
            K_els = get_normalized_elements(K)
            
            int_els = H_els.intersection(K_els)
            int_order = len(int_els)
            
            if int_order == 0:
                neg_q = False
            else:
                index_HK = H.order() // int_order
                index_GK = G.order() // K.order()
                neg_q = index_HK > index_GK
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "H_3: The index of K in G is finite",
    "¬Q: The index of H intersection K in H is not finite or is greater than the index of K in G"
]

N_HYP = 3
NEG_Q_INDEX = 3