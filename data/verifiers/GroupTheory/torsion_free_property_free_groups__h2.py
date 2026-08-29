import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        F, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False
        
    # H_2: x is not the identity element of F
    try:
        if hasattr(F, 'identity'):
            h2 = (x != F.identity)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The element x has finite order (i.e., does NOT have infinite order)
    try:
        finite_order = False
        if hasattr(x, 'order'):
            o = x.order() if callable(x.order) else x.order
            if o != sympy.oo and o != float('inf') and o != 0:
                finite_order = True
        elif isinstance(x, Permutation):
            finite_order = True
        elif hasattr(x, 'is_Matrix') and x.is_Matrix:
            I = eye(x.shape[0])
            curr = x
            for k in range(1, 21):
                if curr == I:
                    finite_order = True
                    break
                curr = curr * x
        elif hasattr(x, 'is_identity') and x.is_identity:
            finite_order = True
            
        neg_q = finite_order
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x is not the identity element of F",
    "¬Q: The element x has finite order"
]

N_HYP = 2
NEG_Q_INDEX = 2