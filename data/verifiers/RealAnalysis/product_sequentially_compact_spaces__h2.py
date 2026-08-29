import sympy
from sympy import Interval, Reals, FiniteSet, Union, Intersection, oo
from sympy.abc import x, y, z
import math
import itertools
import functools

def is_compact(S):
    if isinstance(S, str):
        return S.lower() in ["compact", "sequentially compact", "closed and bounded"]
    
    try:
        if S.is_empty:
            return True
    except Exception:
        pass
    
    bounded = False
    try:
        if hasattr(S, 'is_bounded') and S.is_bounded is not None:
            bounded = bool(S.is_bounded)
        else:
            bounded = bool(S.inf.is_finite and S.sup.is_finite)
    except Exception:
        pass
        
    closed = False
    try:
        if hasattr(S, 'is_closed') and S.is_closed is not None:
            closed = bool(S.is_closed)
        elif hasattr(S, 'boundary'):
            closed = bool(S.boundary.is_subset(S))
    except Exception:
        pass
        
    return bounded and closed

def is_empty_set(S):
    if isinstance(S, str):
        return S.lower() in ["empty", "emptyset", "empty set"]
    try:
        return bool(S.is_empty)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            X = witness.get('X', witness.get('x'))
            Y = witness.get('Y', witness.get('y'))
            if X is None or Y is None:
                return [False, False]
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            X, Y = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = is_compact(X)
    except Exception:
        h1 = False
        
    try:
        if is_empty_set(X) or is_empty_set(Y):
            prod_compact = True
        else:
            prod_compact = is_compact(X) and is_compact(Y)
            
        neg_q = not prod_compact
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) is a sequentially compact metric space",
    "¬Q: X \\times Y is not sequentially compact"
]

N_HYP = 1
NEG_Q_INDEX = 1