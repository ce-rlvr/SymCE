import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def direct_product(G, H):
    degG = G.degree
    degH = H.degree
    if degG == 0: degG = 1
    if degH == 0: degH = 1
    
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr += list(range(len(arr), degG))
        arr += list(range(degG, degG + degH))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(degG))
        h_arr = list(h.array_form)
        if len(h_arr) < degH:
            h_arr += list(range(len(h_arr), degH))
        arr += [x + degG for x in h_arr]
        gens.append(Permutation(arr))
        
    if not gens:
        return PermutationGroup([Permutation(degG + degH - 1)])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False]
        G, H, K, L = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              isinstance(K, PermutationGroup) and 
              isinstance(L, PermutationGroup))
    except Exception:
        h1 = False

    try:
        h2 = bool(K.is_isomorphic(L))
    except Exception:
        h2 = False

    try:
        GxK = direct_product(G, K)
        HxL = direct_product(H, L)
        neg_q = not bool(GxK.is_isomorphic(HxL))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G, H, K, and L are groups",
    "H_2: K is isomorphic to L",
    "¬Q: G x K is not isomorphic to H x L"
]

N_HYP = 2
NEG_Q_INDEX = 2