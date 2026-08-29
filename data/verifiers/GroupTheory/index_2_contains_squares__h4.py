import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
        if len(witness) != 3:
            return [False, False, False, False]
        G, H, g = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            try:
                h2 = H.is_subgroup(G)
            except Exception:
                h2 = all(gen in G for gen in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: The index of H in G is equal to 2
    try:
        g_order = G.order() if callable(G.order) else G.order
        h_order = H.order() if callable(H.order) else H.order
        h3 = (g_order == 2 * h_order)
    except Exception:
        h3 = False
        
    # neg_Q: The element g^2 is not in H
    try:
        g2 = g**2
        try:
            in_H = bool(g2 in H)
        except Exception:
            in_H = False
        neg_q = not in_H
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is equal to 2",
    "¬Q: The element g^2 is not in H"
]

N_HYP = 3
NEG_Q_INDEX = 3