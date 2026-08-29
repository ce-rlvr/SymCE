import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, dict):
            if 'is_F_free_group' in witness:
                h1 = bool(witness.get('is_F_free_group', False))
                h2 = bool(witness.get('is_H_fg_subgroup', False))
                neg_q = not bool(witness.get('is_intersection_fg', True))
                return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_F_free_group'):
            h1 = bool(witness.is_F_free_group)
            h2 = bool(getattr(witness, 'is_H_fg_subgroup', False))
            neg_q = not bool(getattr(witness, 'is_intersection_fg', True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        F, H, K = witness
        
        if type(F).__name__ == 'FreeGroup' or getattr(F, 'is_free_group', False):
            h1 = True
        elif type(F).__name__ == 'FpGroup' and len(F.relators) == 0:
            h1 = True
            
        if isinstance(H, (list, tuple, set)):
            h2 = all(g in F for g in H)
        elif type(H).__name__ == 'FreeGroup':
            h2 = True
        elif type(H).__name__ == 'FpGroup' and len(H.relators) == 0:
            h2 = True
        elif getattr(H, 'is_finitely_generated', False):
            h2 = True
            
        if hasattr(K, 'intersection'):
            H_cap_K = K.intersection(H)
            neg_q = not getattr(H_cap_K, 'is_finitely_generated', True)
        elif hasattr(K, 'is_intersection_fg'):
            neg_q = not K.is_intersection_fg(H)
        else:
            neg_q = not getattr(K, 'is_finitely_generated', True)
            
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: H is a finitely generated subgroup of F",
    "¬Q: The intersection H \\cap K is not a finitely generated subgroup of F"
]

N_HYP = 2
NEG_Q_INDEX = 2