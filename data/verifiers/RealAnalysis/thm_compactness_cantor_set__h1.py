import sympy
from sympy import Set, S, Interval, Union, Intersection, FiniteSet
from sympy.abc import x, y, z

# Top-level setup
R = S.Reals
N = S.Naturals
Z = S.Integers
Q = S.Rationals

def conditions(witness) -> list[bool]:
    try:
        C = witness
        
        # Witness must be a SymPy Set
        if not isinstance(C, Set):
            return [False]
            
        # Witness must be a subset of the Reals
        is_sub = C.is_subset(S.Reals)
        if is_sub is not True:
            return [False]
            
        # Check compactness (in R, compact iff closed and bounded)
        if C == S.EmptySet:
            is_compact = True
        else:
            # Check boundedness
            try:
                is_bounded = (C.inf.is_finite is True) and (C.sup.is_finite is True)
            except Exception:
                is_bounded = False
                
            # Check closedness
            try:
                is_closed = (C.boundary.is_subset(C) is True)
            except Exception:
                try:
                    is_closed = (C.closure == C)
                except Exception:
                    is_closed = False
                    
            is_compact = is_bounded and is_closed
            
        # The conclusion is "C is a compact subset of R"
        # The negated conclusion is True if C is NOT compact
        neg_q = not is_compact
        
    except Exception:
        neg_q = False

    return [bool(neg_q)]

CONDITION_LABELS = ["¬Q: C is not a compact subset of R"]
N_HYP = 0
NEG_Q_INDEX = 0