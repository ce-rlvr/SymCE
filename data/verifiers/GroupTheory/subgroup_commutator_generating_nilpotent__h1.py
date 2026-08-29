import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            h1 = False
        else:
            h1 = bool(all(g in G for g in H.generators))
    except Exception:
        h1 = False

    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            h2 = False
        else:
            K = G.derived_subgroup()
            gens = list(H.generators) + list(K.generators)
            if not gens:
                HK_order = 1
            else:
                HK = PermutationGroup(gens)
                HK_order = HK.order()
            h2 = bool(HK_order == G.order() and all(g in G for g in gens))
    except Exception:
        h2 = False

    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            is_eq = (H.order() == G.order() and 
                     all(g in G for g in H.generators) and 
                     all(g in H for g in G.generators))
            neg_q = not is_eq
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The product of H and the commutator subgroup of G is equal to G",
    "¬Q: H is not equal to G"
]

N_HYP = 2
NEG_Q_INDEX = 2