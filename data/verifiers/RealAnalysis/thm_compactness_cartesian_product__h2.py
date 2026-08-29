import sympy
from sympy import Interval, FiniteSet, Union, Intersection, ProductSet, Reals, EmptySet, Set, oo

# Top-level setup for witness expressions
# Exposing standard set objects and infinity for RealAnalysis witnesses

def is_compact(S):
    """Helper to check if a sympy Set is compact (closed and bounded)."""
    if not isinstance(S, Set):
        return False
    if S.is_empty == True:
        return True
    if isinstance(S, ProductSet):
        return all(is_compact(arg) for arg in S.args)
    try:
        if S.is_bounded == True and S.is_closed == True:
            return True
        if S.is_bounded == False or S.is_closed == False:
            return False
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: A is a compact subset of R^n
    try:
        h1 = bool(is_compact(A))
    except Exception:
        h1 = False
        
    # ¬Q: A x B is NOT a compact subset of R^{n+m}
    try:
        AxB = A * B
        neg_q = not bool(is_compact(AxB))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a compact subset of R^n",
    "¬Q: A x B is not a compact subset of R^{n+m}"
]

N_HYP = 1
NEG_Q_INDEX = 1