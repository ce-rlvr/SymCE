import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(G):
    if isinstance(G, PermutationGroup):
        return True
    cname = G.__class__.__name__
    if cname in ('FreeGroup', 'FpGroup'):
        return True
    return False

def is_non_trivial(G):
    if not is_group(G):
        return False
    if isinstance(G, PermutationGroup):
        return G.order() > 1
    cname = G.__class__.__name__
    if cname == 'FreeGroup':
        return len(G.generators) > 0
    if cname == 'FpGroup':
        if len(G.generators) == 0:
            return False
        if len(G.relators) == 0:
            return True
        try:
            return G.order() > 1
        except Exception:
            return True
    return False

def is_free_group(G):
    cname = G.__class__.__name__
    if cname == 'FreeGroup':
        return True
    if isinstance(G, PermutationGroup):
        return G.order() == 1
    if cname == 'FpGroup':
        return len(G.relators) == 0
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        F1, F2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(is_group(F1) and is_group(F2) and is_non_trivial(F1) and is_non_trivial(F2))
    except Exception:
        h1 = False
        
    try:
        if not (is_group(F1) and is_group(F2)):
            neg_q = False
        else:
            t1 = not is_non_trivial(F1)
            t2 = not is_non_trivial(F2)
            
            if t1 and t2:
                neg_q = True
            elif t1:
                neg_q = bool(is_free_group(F2))
            elif t2:
                neg_q = bool(is_free_group(F1))
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F1 and F2 are non-trivial groups",
    "¬Q: F1 x F2 is a free group"
]

N_HYP = 1
NEG_Q_INDEX = 1