import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy import S, ZZ, QQ, RR, CC, eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z = S.Integers
Q = S.Rationals

def is_periodic(grp):
    """Helper to determine if a group is periodic (all elements have finite order)."""
    if isinstance(grp, PermutationGroup):
        return True
    if grp in (S.Integers, S.Rationals, S.Reals, S.Complexes, ZZ, QQ, RR, CC):
        return False
        
    grp_type = type(grp).__name__
    if grp_type == 'FreeGroup':
        return len(grp.generators) == 0
    if grp_type == 'FpGroup':
        try:
            return grp.order() != S.Infinity
        except Exception:
            return False
            
    if isinstance(grp, str):
        g = grp.lower()
        if g in ['z', 'q', 'r', 'c', 'zz', 'qq', 'rr', 'cc', 'integers', 'rationals']:
            return False
        if 'free' in g:
            return False
        if g in ['z2', 'z3', 'z4', 'z6', 's3', 's4', 'a4', 'd4', 'v4', 'trivial']:
            return True
            
    if hasattr(grp, 'is_finite'):
        if grp.is_finite:
            return True
        if grp.is_finite is False:
            return False
            
    if hasattr(grp, 'order'):
        try:
            if callable(grp.order):
                return grp.order() != S.Infinity
            else:
                return grp.order != S.Infinity
        except Exception:
            pass
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False]
        if len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(is_periodic(H))
    except Exception:
        h1_ok = False
        
    try:
        # G x H is periodic if and only if both G and H are periodic.
        # The negated conclusion requires G x H to NOT be periodic.
        neg_q = not (is_periodic(G) and is_periodic(H))
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a periodic group",
    "¬Q: G x H is not a periodic group"
]

N_HYP = 1
NEG_Q_INDEX = 1