import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(sub, grp):
    try:
        return all(grp.contains(g) for g in sub.generators)
    except Exception:
        return False

def is_normal_subgroup(sub, grp):
    try:
        if not is_subgroup(sub, grp):
            return False
        for h in sub.generators:
            for g in grp.generators:
                if not sub.contains(g * h * (~g)):
                    return False
                if not sub.contains((~g) * h * g):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        if len(witness) != 3:
            return [False, False]
        
        G, N, H = witness
        
        if not all(isinstance(grp, PermutationGroup) for grp in (G, N, H)):
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1_ok = is_normal_subgroup(N, G) and is_subgroup(H, G)
    except Exception:
        h1_ok = False

    try:
        e_normal = is_normal_subgroup(H, G)
        NH = PermutationGroup(list(N.generators) + list(H.generators))
        gal_ke_normal = is_normal_subgroup(NH, G)
        neg_q_ok = (e_normal != gal_ke_normal)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension",
    "¬Q: E/F is normal XOR Gal(K/E) is normal in Gal(K/F)"
]

N_HYP = 1
NEG_Q_INDEX = 1