import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              set(H.elements).issubset(set(G.elements)))
    except Exception:
        h1 = False

    try:
        G, H = witness
        union_of_conjugates = set()
        for g in G.elements:
            g_inv = ~g
            for h in H.elements:
                union_of_conjugates.add(g * h * g_inv)
        
        # The conclusion states the union is a proper subset of G.
        # The negation is that it is NOT a proper subset.
        # Since the union of subgroups is always a subset of G, 
        # not being a proper subset means it is equal to G.
        neg_q = (union_of_conjugates == set(G.elements))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and H is a subgroup of G",
    "¬Q: The union of all conjugate subgroups gHg^{-1} is not a proper subset of G"
]

N_HYP = 1
NEG_Q_INDEX = 1