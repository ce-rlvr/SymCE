import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def direct_product(G, H):
    deg_G = G.degree
    deg_H = H.degree
    if deg_G == 0: deg_G = 1
    if deg_H == 0: deg_H = 1
    
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < deg_G:
            arr += list(range(len(arr), deg_G))
        arr += list(range(deg_G, deg_G + deg_H))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(deg_G))
        h_arr = list(h.array_form)
        if len(h_arr) < deg_H:
            h_arr += list(range(len(h_arr), deg_H))
        arr += [x + deg_G for x in h_arr]
        gens.append(Permutation(arr))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def check_nilpotent(grp):
    val = grp.is_nilpotent
    if callable(val):
        return bool(val())
    return bool(val)

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = check_nilpotent(G)
    except Exception:
        h1 = False
        
    try:
        GxH = direct_product(G, H)
        neg_q = not check_nilpotent(GxH)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a residually nilpotent group",
    "¬Q: G x H is not a residually nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1