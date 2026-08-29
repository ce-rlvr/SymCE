import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1 = False
        if hasattr(H, 'is_subgroup'):
            try:
                h1 = H.is_subgroup(G, strict=False)
            except Exception:
                try:
                    h1 = H.is_subgroup(G)
                except Exception:
                    pass
        if not h1 and hasattr(H, 'generators'):
            try:
                h1 = all(g in G for g in H.generators)
            except Exception:
                pass
    except Exception:
        h1 = False
        
    # neg_Q: The intersection H ∩ Z(G) is NOT a subgroup of Z(H)
    try:
        Z_G = G.center()
        Z_H = H.center()
        
        is_subgroup = True
        # Since H and Z(G) are subgroups, their intersection is a subgroup.
        # We just need to check if it is a subset of Z(H).
        for g in H.generate():
            if g in Z_G:
                if g not in Z_H:
                    is_subgroup = False
                    break
                    
        neg_q = not is_subgroup
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H ∩ Z(G) is not a subgroup of Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1