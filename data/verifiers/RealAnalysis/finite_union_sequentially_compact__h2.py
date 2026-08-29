import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet

# Top-level setup
R = S.Reals
Z = S.Integers
N = S.Naturals
Q = S.Rationals
Empty = S.EmptySet

def is_compact(s):
    try:
        if s == S.EmptySet:
            return True
        if not s.is_subset(S.Reals):
            return False
        if not (s.inf.is_real and s.sup.is_real):
            return False
        if not s.boundary.is_subset(s):
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        A, B = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(is_compact(A))
    except Exception:
        h1 = False
        
    try:
        neg_q = not bool(is_compact(A.union(B)))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a sequentially compact subset of R",
    "¬Q: A U B is not a sequentially compact subset of R"
]

N_HYP = 1
NEG_Q_INDEX = 1