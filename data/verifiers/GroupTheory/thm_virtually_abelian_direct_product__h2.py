import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        # The witness should provide both G and H
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
            
        def is_group(grp):
            if isinstance(grp, (tuple, list)):
                if not grp: return False
                return all(is_group(g) for g in grp)
            if hasattr(grp, 'generators') and hasattr(grp, 'identity'):
                return True
            group_types = ('PermutationGroup', 'FreeGroup', 'FpGroup', 
                           'SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup')
            if type(grp).__name__ in group_types:
                return True
            return False

        def is_virtually_abelian(grp):
            if isinstance(grp, (tuple, list)):
                return all(is_virtually_abelian(g) for g in grp)
            try:
                if getattr(grp, 'is_finite', False):
                    return True
            except Exception:
                pass
            try:
                if callable(getattr(grp, 'order', None)):
                    if grp.order() != sympy.oo:
                        return True
            except Exception:
                pass
            try:
                if getattr(grp, 'is_abelian', False):
                    return True
            except Exception:
                pass
            if type(grp).__name__ == 'FreeGroup':
                return len(grp.generators) <= 1
            return False

        # Hypothesis 1: G is a virtually abelian group
        h1 = is_group(G) and is_virtually_abelian(G)
        
        # Conclusion: The direct product G x H is a virtually abelian group.
        # A direct product of groups is virtually abelian if and only if 
        # both factor groups are virtually abelian.
        is_H_group = is_group(H)
        q = is_virtually_abelian(G) and is_virtually_abelian(H)
        
        # Negated conclusion: G x H is NOT virtually abelian
        neg_q = is_H_group and not q
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a virtually abelian group",
    "¬Q: The direct product G x H is not a virtually abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1