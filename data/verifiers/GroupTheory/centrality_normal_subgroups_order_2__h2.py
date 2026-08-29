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

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: The order of N is 2
    try:
        if isinstance(N, PermutationGroup):
            h2 = (N.order() == 2) and all(g in G for g in N.generators)
        elif isinstance(N, list):
            h2 = (len(N) == 2) and all(g in G for g in N)
            if h2:
                has_id = any(g.is_Identity for g in N)
                h2 = h2 and has_id
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: N is NOT a subgroup of Z(G)
    try:
        neg_q = False
        if isinstance(N, PermutationGroup):
            n_gens = N.generators
        elif isinstance(N, list):
            n_gens = N
        else:
            n_gens = []
            
        for n in n_gens:
            for g in G.generators:
                if n * g != g * n:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The order of N is 2",
    "¬Q: N is not a subgroup of the center Z(G) of G"
]

N_HYP = 2
NEG_Q_INDEX = 2