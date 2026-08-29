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

def conditions(witness) -> list[bool]:
    try:
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False
        
    # H_2: x and y are elements of G
    try:
        h2 = bool((x in G) and (y in G))
    except Exception:
        h2 = False
        
    # H_3: x and y are conjugate in G
    try:
        h3 = False
        if h2:
            for g in G.generate():
                if g * x * ~g == y:
                    h3 = True
                    break
    except Exception:
        h3 = False
        
    # neg_Q: xN and yN are not conjugate in G/N
    try:
        neg_q = False
        if h1 and h2:
            neg_q = True
            for g in G.generate():
                val = g * x * ~g * ~y
                if val in N:
                    neg_q = False
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: x and y are elements of G",
    "H_3: x and y are conjugate in G",
    "¬Q: xN and yN are not conjugate in G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3