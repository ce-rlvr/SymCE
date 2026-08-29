import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: It is not the case that H is a normal subgroup of G iff H is a union of conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: H is a subgroup of G
    try:
        h1_ok = False
        if hasattr(H, 'is_subgroup'):
            h1_ok = bool(H.is_subgroup(G))
        else:
            H_elements = set(H)
            G_elements = set(G.elements)
            if H_elements.issubset(G_elements) and len(H_elements) > 0:
                if G.identity in H_elements:
                    closed = True
                    for a in H_elements:
                        if a**-1 not in H_elements:
                            closed = False
                            break
                        for b in H_elements:
                            if a * b not in H_elements:
                                closed = False
                                break
                        if not closed:
                            break
                    h1_ok = closed
    except Exception:
        h1_ok = False

    # neg_Q: Not ( (H is a normal subgroup of G) iff (H is a union of conjugacy classes of G) )
    try:
        G_elements = set(G.elements)
        H_elements = set(H.elements) if hasattr(H, 'elements') else set(H)
        
        # Check if H is a normal subgroup
        is_normal = False
        if h1_ok:
            if hasattr(H, 'is_normal'):
                is_normal = bool(H.is_normal(G))
            else:
                is_normal = True
                for g in G_elements:
                    for h in H_elements:
                        if g * h * g**-1 not in H_elements:
                            is_normal = False
                            break
                    if not is_normal:
                        break
        
        # Check if H is a union of conjugacy classes of G
        is_union = False
        if H_elements.issubset(G_elements):
            is_union = True
            for g in G_elements:
                for h in H_elements:
                    if g * h * g**-1 not in H_elements:
                        is_union = False
                        break
                if not is_union:
                    break
                    
        neg_q_ok = not (is_normal == is_union)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]