import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, oo

# Top-level setup
Reals = S.Reals
EmptySet = S.EmptySet

def is_closed(s):
    try:
        if s == S.EmptySet or s == S.Reals:
            return True
        b = s.boundary
        return bool(b.is_subset(s))
    except Exception:
        return False

def is_bounded(s):
    try:
        if s == S.EmptySet:
            return True
        return bool(s.inf.is_finite and s.sup.is_finite)
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        K, F = witness
    except Exception:
        return [False, False, False]
    
    # H_1: K is a sequentially compact subset of R
    try:
        h1 = bool(K.is_subset(S.Reals) and is_closed(K) and is_bounded(K))
    except Exception:
        h1 = False
        
    # H_2: F is closed in R
    try:
        h2 = bool(F.is_subset(S.Reals) and is_closed(F))
    except Exception:
        h2 = False
        
    # ¬Q: F is not sequentially compact
    try:
        q = bool(F.is_subset(S.Reals) and is_closed(F) and is_bounded(F))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a sequentially compact subset of R",
    "H_2: F is closed in R",
    "¬Q: F is not sequentially compact"
]

N_HYP = 2
NEG_Q_INDEX = 2