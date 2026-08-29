import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_subgroup(H, G):
    try:
        return all(h in G for h in H.generators)
    except Exception:
        return False

def is_normal(H, G):
    try:
        if not is_subgroup(H, G):
            return False
        for h in H.generators:
            for g in G.generators:
                if (g * h * ~g) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G, H, and K are groups (represented as PermutationGroups)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H and K are normal subgroups of G
    try:
        h2 = is_normal(H, G) and is_normal(K, G)
    except Exception:
        h2 = False

    # H3: K is a solvable group
    try:
        h3 = bool(K.is_solvable)
    except Exception:
        h3 = False

    # neg_Q: HK is not a normal solvable subgroup of G
    try:
        HK_gens = list(H.generators) + list(K.generators)
        HK = PermutationGroup(HK_gens)
        
        is_HK_normal = is_normal(HK, G)
        is_HK_solvable = bool(HK.is_solvable)
        
        q = is_HK_normal and is_HK_solvable
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G, H, and K are groups",
    "H_2: H and K are normal subgroups of G",
    "H_3: K is a solvable group",
    "¬Q: HK is not a normal solvable subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3