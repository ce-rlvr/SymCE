import sympy
from sympy import S, FiniteSet, Interval, Union, Intersection
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
R = S.Reals
N = S.Naturals
Z = S.Integers
Q = S.Rationals

def conditions(witness) -> list[bool]:
    try:
        A, pt = witness
    except Exception:
        return [False, False]
    
    # H_1: A is a subset of the real numbers
    try:
        if not isinstance(A, sympy.Set):
            h1 = False
        else:
            h1 = bool(A.is_subset(S.Reals)) and (pt in S.Reals)
    except Exception:
        h1 = False
        
    # neg_Q: There does NOT exist a sequence in A \ {x} converging to x
    # This is equivalent to saying that x is NOT an accumulation point of A.
    try:
        if not isinstance(A, sympy.Set):
            neg_q = False
        else:
            A_minus_pt = A - FiniteSet(pt)
            closure = A_minus_pt.closure
            pt_is_acc_pt = closure.contains(pt)
            if pt_is_acc_pt is None:
                neg_q = False
            else:
                neg_q = not bool(pt_is_acc_pt)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a subset of the real numbers",
    "¬Q: There does not exist a sequence in A \\ {x} converging to x"
]

N_HYP = 1
NEG_Q_INDEX = 1