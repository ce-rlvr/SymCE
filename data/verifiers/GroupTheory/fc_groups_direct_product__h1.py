import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
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

def is_fc_group(G):
    if hasattr(G, 'is_finite') and G.is_finite:
        return True
    if hasattr(G, 'is_abelian') and G.is_abelian:
        return True
    if isinstance(G, PermutationGroup):
        return True
    if type(G).__name__ == 'FreeGroup':
        return len(G.generators) <= 1
    if type(G).__name__ == 'FpGroup':
        try:
            if G.order() != float('inf'):
                return True
        except Exception:
            pass
        if len(G.relators) == 0 and len(G.generators) > 1:
            return False
    raise ValueError("Cannot determine FC property for the given group")

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(is_fc_group(H))
    except Exception:
        h1 = False
        
    try:
        g_fc = is_fc_group(G)
        h_fc = is_fc_group(H)
        neg_q = not (g_fc and h_fc)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is an FC-group",
    "¬Q: The direct product G x H is not an FC-group"
]

N_HYP = 1
NEG_Q_INDEX = 1