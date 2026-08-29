import sympy
from sympy import Set, Interval, FiniteSet, Union, Intersection, S

def derived_set(s):
    if getattr(s, 'is_FiniteSet', False):
        return S.EmptySet
    if s in (S.Integers, S.Naturals, S.Naturals0):
        return S.EmptySet
    if isinstance(s, Interval):
        if s.start == s.end:
            return S.EmptySet
        return Interval(s.start, s.end, False, False)
    if isinstance(s, Union):
        return Union(*[derived_set(arg) for arg in s.args])
    if s == S.Reals:
        return S.Reals
    if s == S.Rationals:
        return S.Reals
    try:
        return s.closure
    except Exception:
        return s

def is_bounded(s):
    if s == S.EmptySet:
        return True
    if getattr(s, 'is_FiniteSet', False):
        return True
    if s == S.Reals:
        return False
    if s in (S.Integers, S.Naturals, S.Naturals0):
        return False
    if isinstance(s, Interval):
        return s.start.is_finite and s.end.is_finite
    if isinstance(s, Union):
        return all(is_bounded(arg) for arg in s.args)
    try:
        b = s.is_bounded
        if b is not None:
            return b
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let (X, d) be a metric space. The derived set K' is a compact subset of X."
    
    The witness is expected to be a subset K of R (which acts as our metric space X).
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        X, K = witness
    else:
        X, K = S.Reals, witness

    try:
        h1 = isinstance(K, Set)
    except Exception:
        h1 = False

    try:
        ds = derived_set(K)
        # In R, a closed set (like a derived set) is compact iff it is bounded.
        # The conclusion fails (neg_Q is True) if the derived set is NOT bounded.
        neg_q = not is_bounded(ds)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a subset of a metric space",
    "¬Q: The derived set K' is not compact"
]

N_HYP = 1
NEG_Q_INDEX = 1