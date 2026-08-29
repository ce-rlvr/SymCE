import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    try:
        h2 = all(g in G for g in K.generators)
    except Exception:
        h2 = False

    try:
        elements_H = list(H.elements)
        elements_K = list(K.elements)
        
        gens_HK = []
        for h in elements_H:
            for k in elements_K:
                gens_HK.append((~h) * (~k) * h * k)
        HK = PermutationGroup(gens_HK)
        
        gens_KH = []
        for k in elements_K:
            for h in elements_H:
                gens_KH.append((~k) * (~h) * k * h)
        KH = PermutationGroup(gens_KH)
        
        neg_q = not (HK == KH)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "¬Q: The commutator subgroup of H and K is not equal to the commutator subgroup of K and H"
]

N_HYP = 2
NEG_Q_INDEX = 2