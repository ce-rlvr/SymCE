import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, EmptySet, Set

# Top-level setup for witness expressions
Reals = S.Reals

def to_sympy_set(obj):
    if isinstance(obj, Set):
        return obj
    if isinstance(obj, (list, set, tuple)):
        return FiniteSet(*obj)
    raise ValueError("Not a valid set representation")

def conditions(witness):
    try:
        X_raw, U_raw = witness
    except Exception:
        return [False, False, False]
        
    try:
        X = to_sympy_set(X_raw)
    except Exception:
        X = None

    # H1: X is a compact metric space
    h1 = False
    try:
        if X is not None and X != EmptySet:
            # In the real line, a set is compact iff it is closed and bounded
            if X.is_closed == True and X.is_bounded == True:
                h1 = True
    except Exception:
        h1 = False

    # H2: {U_n} is a sequence of open subsets of X
    h2 = False
    try:
        if h1 and isinstance(U_raw, (list, set, tuple)) and len(U_raw) > 0:
            h2 = True
            U = []
            for u_raw in U_raw:
                u = to_sympy_set(u_raw)
                U.append(u)
                if not u.is_subset(X):
                    h2 = False
                    break
                # u is open in X iff X \ u is closed in X.
                # Since X is closed in R, X \ u is closed in X iff it is closed in R.
                comp = X - u
                if comp.is_closed != True:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The intersection of all U_n is NOT dense in X
    neg_q = False
    try:
        if h1 and h2:
            intersect = X
            for u in U:
                intersect = Intersection(intersect, u)
            
            # intersect is dense in X iff X is a subset of the closure of intersect
            closure_int = intersect.closure
            if not X.is_subset(closure_int):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: {U_n} is a sequence of open subsets of X",
    "¬Q: The intersection of all U_n is not dense in X"
]

N_HYP = 2
NEG_Q_INDEX = 2