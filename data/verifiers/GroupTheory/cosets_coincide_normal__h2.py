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
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = True
        H_set = set(H)
        G_elements = set(G.generate())
        if not H_set.issubset(G_elements):
            h2 = False
        else:
            for g in G_elements:
                gH = set(g * h for h in H_set)
                Hg = set(h * g for h in H_set)
                if gH != Hg:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    try:
        is_subgroup = True
        H_set = set(H)
        G_elements = set(G.generate())
        
        if not H_set:
            is_subgroup = False
        elif G.identity not in H_set:
            is_subgroup = False
        else:
            for h1_elem in H_set:
                for h2_elem in H_set:
                    if h1_elem * h2_elem not in H_set:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        if is_subgroup:
            is_normal = True
            for g in G_elements:
                for h_elem in H_set:
                    if ~g * h_elem * g not in H_set:
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
            
        neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: For every g in G, the left coset gH equals the right coset Hg",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2