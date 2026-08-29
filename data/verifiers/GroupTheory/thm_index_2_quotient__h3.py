import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not (isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup)):
            h2 = False
        else:
            try:
                h2 = bool(H.is_subgroup(G))
            except Exception:
                h2 = all(g in G for g in H.generators)
    except Exception:
        h2 = False

    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            neg_q = False
        else:
            try:
                is_sub = bool(H.is_subgroup(G))
            except Exception:
                is_sub = all(g in G for g in H.generators)
                
            if not is_sub:
                is_normal = False
            else:
                try:
                    is_normal = bool(H.is_normal(G))
                except Exception:
                    is_normal = all((g**-1 * h * g) in H for g in G.generators for h in H.generators)
            
            try:
                g_order = G.order()
            except Exception:
                g_order = len(list(G.generate()))
                
            try:
                h_order = H.order()
            except Exception:
                h_order = len(list(H.generate()))
                
            index_is_2 = (g_order == 2 * h_order)
            q = is_normal and index_is_2
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not a normal subgroup of G or G/H is not isomorphic to Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2