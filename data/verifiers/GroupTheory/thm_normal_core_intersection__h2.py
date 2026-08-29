import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for witness expressions
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
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group and H is a subset of G
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, (list, set, tuple))
        if h1_ok:
            for h in H:
                if h not in G:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # neg_Q: The intersection of conjugates of H is NOT the largest normal subgroup of G contained in H
    try:
        if not h1_ok:
            neg_q = False
        else:
            elements_G = list(G.elements)
            
            # Calculate the intersection I = \bigcap_{g \in G} gHg^{-1}
            I = set(H)
            for g in elements_G:
                g_inv = ~g
                gHg_inv = {g * h * g_inv for h in H}
                I = I.intersection(gHg_inv)
                if not I:
                    break
            
            # Check if I is a subgroup of G.
            # Since G is finite, I is a subgroup iff it is non-empty, contains the identity, 
            # and is closed under multiplication.
            # If I is a subgroup, it is automatically normal (by definition of I) 
            # and contains all normal subgroups contained in H, making the conclusion TRUE.
            # Thus, the conclusion FAILS (neg_Q is True) iff I is NOT a subgroup.
            is_subgroup = True
            if not I:
                is_subgroup = False
            elif G.identity not in I:
                is_subgroup = False
            else:
                for a in I:
                    for b in I:
                        if a * b not in I:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and H is a subset of G",
    "¬Q: The intersection of conjugates of H is not the largest normal subgroup of G contained in H"
]

N_HYP = 1
NEG_Q_INDEX = 1