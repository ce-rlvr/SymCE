import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
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

def is_group(G):
    if hasattr(G, 'is_group'):
        val = G.is_group() if callable(G.is_group) else G.is_group
        if val: 
            return True
    group_types = ('PermutationGroup', 'FpGroup', 'FreeGroup', 'NamedGroup')
    if any(type(G).__name__ == t for t in group_types) or any(base.__name__ in group_types for base in type(G).__mro__):
        return True
    if hasattr(G, 'generators') and hasattr(G, 'order'):
        return True
    return False

def is_virtually_nilpotent(grp):
    if hasattr(grp, 'is_virtually_nilpotent'):
        val = grp.is_virtually_nilpotent() if callable(grp.is_virtually_nilpotent) else grp.is_virtually_nilpotent
        if val is not None:
            return bool(val)
            
    if hasattr(grp, 'is_nilpotent'):
        val = grp.is_nilpotent() if callable(grp.is_nilpotent) else grp.is_nilpotent
        if val:
            return True
            
    try:
        if grp.order() < float('inf'):
            return True
    except Exception:
        pass
        
    try:
        if getattr(grp, 'is_finite', False):
            return True
    except Exception:
        pass

    if type(grp).__name__ == 'FreeGroup':
        try:
            if len(grp.generators) <= 1:
                return True
            else:
                return False
        except Exception:
            pass

    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two groups (G, H).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False
        
    # H_2: H is a group
    try:
        h2 = is_group(H)
    except Exception:
        h2 = False
        
    # H_3: G is virtually nilpotent
    try:
        h3 = is_virtually_nilpotent(G)
    except Exception:
        h3 = False
        
    # neg_Q: G x H is NOT virtually nilpotent
    # Mathematically, G x H is virtually nilpotent iff both G and H are virtually nilpotent.
    try:
        g_vn = is_virtually_nilpotent(G)
        h_vn = is_virtually_nilpotent(H)
        neg_q = not (g_vn and h_vn)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: G is virtually nilpotent",
    "¬Q: G x H is not virtually nilpotent"
]

N_HYP = 3
NEG_Q_INDEX = 3