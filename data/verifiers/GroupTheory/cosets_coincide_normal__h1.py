import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H_2: For every g in G, the left coset gH equals the right coset Hg
    try:
        h2 = True
        G_elems = list(G.elements)
        H_elems = list(H.elements)
        for g in G_elems:
            left_coset = set(g * h for h in H_elems)
            right_coset = set(h * g for h in H_elems)
            if left_coset != right_coset:
                h2 = False
                break
    except Exception:
        h2 = False
        
    # ¬Q: H is not a normal subgroup of G
    try:
        neg_q = not bool(H.is_normal(G))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: For every g in G, the left coset gH equals the right coset Hg",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2