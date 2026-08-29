import sympy
from sympy import Set, S, Interval, FiniteSet, Union, Intersection

# Top-level setup
R = S.Reals
Z = S.Integers
N = S.Naturals

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        K, C = witness
    except Exception:
        return [False, False, False]
        
    # H1: K is a compact subset of R^d
    try:
        h1 = False
        if isinstance(K, Set) and K.is_subset(S.Reals) == True:
            is_closed = K.boundary.is_subset(K) == True
            is_bounded = (K.is_empty == True) or (
                hasattr(K, 'inf') and hasattr(K, 'sup') and 
                K.inf.is_finite == True and K.sup.is_finite == True
            )
            h1 = is_closed and is_bounded
    except Exception:
        h1 = False

    # H2: C is a closed subset of R^d
    try:
        h2 = False
        if isinstance(C, Set) and C.is_subset(S.Reals) == True:
            h2 = C.boundary.is_subset(C) == True
    except Exception:
        h2 = False

    # neg_Q: C is not a compact set
    try:
        neg_q = False
        if isinstance(C, Set) and C.is_subset(S.Reals) == True:
            is_closed = C.boundary.is_subset(C) == True
            is_bounded = (C.is_empty == True) or (
                hasattr(C, 'inf') and hasattr(C, 'sup') and 
                C.inf.is_finite == True and C.sup.is_finite == True
            )
            is_compact = is_closed and is_bounded
            neg_q = not is_compact
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^d",
    "H_2: C is a closed subset of R^d",
    "¬Q: C is not a compact set"
]

N_HYP = 2
NEG_Q_INDEX = 2