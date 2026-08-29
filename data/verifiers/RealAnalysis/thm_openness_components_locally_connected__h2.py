import sympy
from sympy import Interval, FiniteSet, Union, Intersection, S

# Top-level setup
R = S.Reals
Z = S.Integers
N = S.Naturals
Empty = S.EmptySet

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        X, C = witness
    except Exception:
        return [False, False]
        
    # H1: X is a locally connected topological space
    try:
        # We restrict to subsets of the real line for this domain.
        # A subset of R is locally connected if it is a finite union of intervals and points.
        def is_loc_conn(s):
            if s in (S.Reals, S.Integers, S.EmptySet):
                return True
            if isinstance(s, (Interval, FiniteSet)):
                return True
            if isinstance(s, Union):
                return all(is_loc_conn(arg) for arg in s.args)
            return False
            
        h1 = is_loc_conn(X)
    except Exception:
        h1 = False
        
    # neg_Q: C is NOT an open subset of X
    try:
        is_subset = C.is_subset(X)
        if is_subset is False:
            # If C is not a subset of X, it cannot be an open subset of X.
            is_open_in_X = False
        elif is_subset is True:
            # C is open in X iff C is disjoint from the closure of (X \ C) in R.
            diff = X - C
            if hasattr(diff, 'closure'):
                diff_closure = diff.closure
            else:
                diff_closure = diff
            
            inter = Intersection(C, diff_closure)
            if inter.is_empty is True:
                is_open_in_X = True
            elif inter.is_empty is False:
                is_open_in_X = False
            else:
                # If sympy cannot decide, assume it is open to prevent false positive counterexamples
                is_open_in_X = True
        else:
            # If subset status is undecidable, assume it is open to prevent false positive
            is_open_in_X = True
            
        neg_q = not is_open_in_X
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a locally connected topological space",
    "¬Q: C is not an open subset of X"
]

N_HYP = 1
NEG_Q_INDEX = 1