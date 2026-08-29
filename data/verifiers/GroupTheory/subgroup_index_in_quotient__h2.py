import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
        
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
        
    # H_3: N \subseteq H
    try:
        if isinstance(N, PermutationGroup):
            h3 = N.is_subgroup(H)
        else:
            h3 = all(elem in H for elem in N)
    except Exception:
        h3 = False
        
    # neg_Q: The index of H in G is equal to the index of H/N in G/N
    # The conclusion fails (neg_Q is True) if G/N or H/N are not valid quotient groups,
    # which happens when N is not a normal subgroup of G (or H).
    try:
        if isinstance(N, PermutationGroup):
            N_group = N
            is_N_group = True
        else:
            N_list = list(N)
            if not N_list:
                is_N_group = False
            else:
                N_group = PermutationGroup(N_list)
                is_N_group = (N_group.order() == len(set(N_list)))
            
        if not is_N_group:
            q = False
        elif not isinstance(H, PermutationGroup) or not H.is_subgroup(G):
            q = False
        elif not N_group.is_subgroup(G):
            q = False
        elif not G.is_normal(N_group):
            q = False
        elif not H.is_normal(N_group):
            q = False
        else:
            idx_GH = G.order() // H.order()
            idx_GN = G.order() // N_group.order()
            idx_HN = H.order() // N_group.order()
            q = (idx_GH == idx_GN // idx_HN)
    except Exception:
        q = False
        
    neg_q = not q
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N is a subset of H",
    "¬Q: The index of H in G is not equal to the index of H/N in G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3