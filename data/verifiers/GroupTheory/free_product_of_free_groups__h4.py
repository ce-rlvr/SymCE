import sympy
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

def is_group(G):
    if hasattr(G, 'is_group') and G.is_group:
        return True
    if hasattr(G, 'is_PermutationGroup') and G.is_PermutationGroup:
        return True
    if type(G).__name__ in ('FreeGroup', 'FpGroup', 'PolycyclicGroup'):
        return True
    return False

def is_free_group(G):
    try:
        if G.order() == 1:
            return True
    except Exception:
        pass
    
    if type(G).__name__ == 'FreeGroup':
        return True
        
    if hasattr(G, 'is_PermutationGroup') and G.is_PermutationGroup:
        return False
        
    if type(G).__name__ == 'FpGroup':
        if len(G.relators) == 0:
            return True
            
    return False

def conditions(witness):
    """
    witness is expected to be a tuple: (I, F_family, F)
    where:
      - I is an index set (list, set, or tuple)
      - F_family is a dict or list mapping indices in I to groups
      - F is a group
    """
    try:
        I, F_family, F = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: I is an index set
    try:
        h1 = isinstance(I, (list, set, tuple))
    except Exception:
        h1 = False
        
    # H_2: {F_i}_{i \in I} is a family of groups
    try:
        if isinstance(F_family, dict):
            h2 = all(i in F_family and is_group(F_family[i]) for i in I)
        elif isinstance(F_family, (list, tuple)):
            h2 = all(isinstance(i, int) and 0 <= i < len(F_family) and is_group(F_family[i]) for i in I)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: For every i \in I, F_i is a free group
    try:
        if isinstance(F_family, dict):
            h3 = all(is_free_group(F_family[i]) for i in I)
        elif isinstance(F_family, (list, tuple)):
            h3 = all(is_free_group(F_family[i]) for i in I)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: F is not a free group
    try:
        neg_q = is_group(F) and not is_free_group(F)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is an index set",
    "H_2: {F_i}_{i \\in I} is a family of groups",
    "H_3: For every i \\in I, F_i is a free group",
    "¬Q: F is not a free group"
]

N_HYP = 3
NEG_Q_INDEX = 3