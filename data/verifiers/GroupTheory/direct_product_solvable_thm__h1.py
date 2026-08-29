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

def direct_product(G, H):
    degG = G.degree
    degH = H.degree
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr += list(range(len(arr), degG))
        p = arr + list(range(degG, degG + degH))
        gens.append(Permutation(p))
    for h in H.generators:
        arr = list(h.array_form)
        if len(arr) < degH:
            arr += list(range(len(arr), degH))
        p = list(range(degG)) + [x + degG for x in arr]
        gens.append(Permutation(p))
    if not gens:
        if degG + degH > 0:
            return PermutationGroup([Permutation(degG + degH - 1)])
        else:
            return PermutationGroup([Permutation()])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        solv_G = G.is_solvable
        h1 = bool(solv_G() if callable(solv_G) else solv_G)
    except Exception:
        h1 = False

    try:
        solv_H = H.is_solvable
        h2 = bool(solv_H() if callable(solv_H) else solv_H)
    except Exception:
        h2 = False

    try:
        GxH = direct_product(G, H)
        solv_GxH = GxH.is_solvable
        neg_q = not bool(solv_GxH() if callable(solv_GxH) else solv_GxH)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: H is a solvable group",
    "¬Q: The direct product G x H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2