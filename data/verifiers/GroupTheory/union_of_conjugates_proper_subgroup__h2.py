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
V4 = DihedralGroup(2)
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

    G_elements = set()
    H_elements = set()
    
    try:
        if isinstance(G, PermutationGroup):
            G_elements = set(G.elements)
            if hasattr(H, 'elements'):
                H_elements = set(H.elements)
            else:
                H_elements = set(H)
            h1 = H_elements.issubset(G_elements)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            h2 = (H_elements != G_elements)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            union_conjugates = set()
            for g in G_elements:
                g_inv = g**-1
                for h in H_elements:
                    union_conjugates.add(g * h * g_inv)
            neg_q = (union_conjugates == G_elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is not equal to G",
    "¬Q: The union of gHg^{-1} over all g in G is equal to G"
]

N_HYP = 2
NEG_Q_INDEX = 2