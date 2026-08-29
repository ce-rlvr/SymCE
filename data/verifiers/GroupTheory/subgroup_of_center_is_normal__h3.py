import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subset of Z(G)
    try:
        if isinstance(H, PermutationGroup):
            elements_H = list(H.elements)
        else:
            elements_H = list(H)
            
        h2 = True
        for h in elements_H:
            if not isinstance(h, Permutation):
                h2 = False
                break
            if h not in G:
                h2 = False
                break
            # Check if h is in Z(G)
            for g in G.generators:
                if h * g != g * h:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        if isinstance(H, PermutationGroup):
            # If H is a PermutationGroup and all its elements are in G, it is a subgroup.
            # Since it's in Z(G) (from H_2), it is automatically normal.
            # Thus, it IS a normal subgroup, so the negated conclusion is False.
            neg_q = False
        else:
            elements_H = list(H)
            is_subgroup = True
            if not elements_H:
                is_subgroup = False
            else:
                identity = G.identity
                if identity not in elements_H:
                    is_subgroup = False
                else:
                    for a in elements_H:
                        if ~a not in elements_H:
                            is_subgroup = False
                            break
                        for b in elements_H:
                            if a * b not in elements_H:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
            # Since H is a subset of Z(G), if it is a subgroup, it is normal.
            # Therefore, H is a normal subgroup iff it is a subgroup.
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subset of Z(G)",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2