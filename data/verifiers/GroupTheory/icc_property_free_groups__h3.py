import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness):
    try:
        # Witness can be a tuple (F, x) or just the element x
        if isinstance(witness, tuple) and len(witness) == 2:
            F, x_elem = witness
        else:
            x_elem = witness
            F = x_elem.group
    except Exception:
        return [False, False, False]

    # H1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # H2: The rank of F is at least 2
    try:
        h2 = False
        if h1:
            h2 = len(F.generators) >= 2
    except Exception:
        h2 = False

    # neg_Q: The conjugacy class of x in F is finite
    try:
        neg_q = False
        if h1 and x_elem in F:
            # In a free group, the conjugacy class of an element is finite 
            # if and only if the group has rank < 2 or the element is the identity.
            is_id = False
            if hasattr(F, 'identity') and x_elem == F.identity:
                is_id = True
            elif hasattr(x_elem, 'is_identity') and x_elem.is_identity:
                is_id = True
            elif hasattr(x_elem, '__len__') and len(x_elem) == 0:
                is_id = True
                
            neg_q = (len(F.generators) < 2) or is_id
        else:
            # Fallback for other types of groups
            if hasattr(F, 'is_finite') and F.is_finite:
                neg_q = True
            elif hasattr(F, 'order') and callable(F.order):
                try:
                    if F.order() < float('inf'):
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: The rank of F is at least 2",
    "¬Q: The conjugacy class of x in F is finite"
]

N_HYP = 2
NEG_Q_INDEX = 2