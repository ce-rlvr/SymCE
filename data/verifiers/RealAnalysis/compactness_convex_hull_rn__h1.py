import sympy
from sympy import Interval, FiniteSet, Union, Intersection, S, Reals, Integers, Naturals, Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The convex hull of K is a compact subset of R^n."
    
    A valid witness is a set K (e.g., a SymPy Set in R) whose convex hull is NOT compact.
    """
    try:
        # We expect the witness to be a SymPy Set in R.
        if not hasattr(witness, 'inf') or not hasattr(witness, 'sup'):
            return [False]
        
        if witness.is_empty:
            hull = witness
        else:
            inf = witness.inf
            sup = witness.sup
            
            # The convex hull of a set in R is the interval between its infimum and supremum.
            # The endpoints are included in the hull iff they are in the original set.
            left_closed = (witness.contains(inf) == True)
            right_closed = (witness.contains(sup) == True)
            
            hull = Interval(inf, sup, left_open=not left_closed, right_open=not right_closed)
        
        # Check if the convex hull is compact (closed and bounded in R)
        if hull.is_empty:
            is_compact = True
        elif isinstance(hull, Interval):
            is_compact = (not hull.left_open) and (not hull.right_open) and (hull.inf != S.NegativeInfinity) and (hull.sup != S.Infinity)
        elif hull.is_FiniteSet:
            is_compact = True
        else:
            is_compact = False
            
        neg_q = not is_compact
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The convex hull of K is not a compact subset of R^n"
]

N_HYP = 0
NEG_Q_INDEX = 0