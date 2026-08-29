import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def is_virtually_solvable(grp):
    """
    Checks if a group is virtually solvable (has a solvable subgroup of finite index).
    """
    # 1. Check for custom attribute/method
    if hasattr(grp, 'is_virtually_solvable'):
        val = grp.is_virtually_solvable
        return val() if callable(val) else bool(val)
        
    cls_name = grp.__class__.__name__
    
    # 2. Free groups are virtually solvable iff their rank is <= 1
    if cls_name == 'FreeGroup':
        return len(grp.generators) <= 1
        
    # 3. Finite permutation groups are always virtually solvable 
    # (the trivial subgroup is solvable and has finite index)
    if cls_name in ('PermutationGroup', 'AlternatingGroup', 'SymmetricGroup', 'DihedralGroup', 'CyclicGroup'):
        return True
        
    # 4. Check if explicitly finite
    if hasattr(grp, 'is_finite'):
        val = grp.is_finite
        val = val() if callable(val) else val
        if val:
            return True
            
    # 5. Check order to see if it's finite
    try:
        from sympy import oo
        ord_val = grp.order() if callable(grp.order) else grp.order
        if ord_val != oo:
            return True
    except Exception:
        pass
        
    # 6. Fallback to checking if the group itself is solvable
    if hasattr(grp, 'is_solvable'):
        val = grp.is_solvable
        val = val() if callable(val) else val
        if val is True:
            return True
            
    raise ValueError(f"Cannot determine virtual solvability for {grp}")

def conditions(witness) -> list[bool]:
    # The conjecture implicitly involves two groups G and H, as H appears in the conclusion.
    # The witness must provide both G and H.
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            if G is None or H is None:
                return [False, False]
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: G is a virtually solvable group
    try:
        h1_ok = is_virtually_solvable(G)
    except Exception:
        h1_ok = False
        
    # ¬Q: The direct product G x H is NOT a virtually solvable group.
    # Mathematically, G x H is virtually solvable if and only if BOTH G and H are virtually solvable.
    try:
        q = is_virtually_solvable(G) and is_virtually_solvable(H)
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a virtually solvable group",
    "¬Q: The direct product G x H is not a virtually solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1