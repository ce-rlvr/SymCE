import sympy
from sympy import S, Interval, FiniteSet, Union, Complement

# Top-level setup for Real Analysis
P = S.Reals - S.Rationals

CONDITION_LABELS = [
    "H_1: witness is the set of irrational numbers P = R \\ Q",
    "¬Q: witness is not totally disconnected"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_totally_disconnected(s):
    """
    Helper function to determine if a SymPy set is totally disconnected.
    """
    try:
        if hasattr(s, 'is_subset'):
            if s.is_subset(S.Reals - S.Rationals) == True:
                return True
            if s.is_subset(S.Rationals) == True:
                return True
            if s.is_subset(S.Integers) == True:
                return True
    except Exception:
        pass
    
    if isinstance(s, FiniteSet):
        return True
    if isinstance(s, Interval):
        return s.start == s.end
    if isinstance(s, Union):
        return all(is_totally_disconnected(arg) for arg in s.args)
    if s == S.Reals - S.Rationals or s == Complement(S.Reals, S.Rationals):
        return True
    if s == S.EmptySet:
        return True
        
    return False

def conditions(witness):
    try:
        # Check if the witness is exactly the set of irrational numbers
        h1 = bool(witness == S.Reals - S.Rationals or witness == Complement(S.Reals, S.Rationals))
    except Exception:
        h1 = False

    try:
        # The conclusion is that the space is totally disconnected.
        # We negate it: the witness is NOT totally disconnected.
        neg_q = not is_totally_disconnected(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]