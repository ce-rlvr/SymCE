import sympy
from sympy import Set, Interval, FiniteSet, Union, Intersection, ProductSet, S, EmptySet

# Top-level setup: named object bindings that the witness expression may reference
Reals = S.Reals
Integers = S.Integers
Naturals = S.Naturals
Rationals = S.Rationals
Complexes = S.Complexes

def is_compact(S_obj):
    """Helper function to determine if a sympy Set represents a compact metric space."""
    if hasattr(S_obj, 'is_compact') and callable(S_obj.is_compact):
        try:
            res = S_obj.is_compact()
            if isinstance(res, bool):
                return res
        except Exception:
            pass
    try:
        if getattr(S_obj, 'is_EmptySet', False) is True:
            return True
        if isinstance(S_obj, FiniteSet):
            return all((getattr(e, 'is_real', False) is True) and (getattr(e, 'is_finite', False) is True) for e in S_obj)
        if isinstance(S_obj, Interval):
            return (not S_obj.left_open) and (not S_obj.right_open) and (S_obj.inf.is_finite is True) and (S_obj.sup.is_finite is True)
        if isinstance(S_obj, Union):
            return all(is_compact(arg) for arg in S_obj.args)
        if isinstance(S_obj, ProductSet):
            return all(is_compact(arg) for arg in S_obj.sets)
        if S_obj in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.Rationals, S.Complexes):
            return False
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # The witness should be a tuple of two metric spaces (X, Y)
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        X, Y = witness
    except Exception:
        return [False, False, False]
        
    # H_1: (Y, d_Y) is a compact metric space
    try:
        h1 = bool(is_compact(Y))
    except Exception:
        h1 = False
        
    # H_2: X x Y is the Cartesian product space equipped with the product metric
    # We verify that X and Y are valid sets/spaces that can form a product space.
    try:
        h2 = bool((isinstance(X, Set) or hasattr(X, 'is_compact')) and \
                  (isinstance(Y, Set) or hasattr(Y, 'is_compact')))
    except Exception:
        h2 = False
        
    # ¬Q: The metric space X x Y is NOT compact
    try:
        x_empty = (getattr(X, 'is_EmptySet', False) is True)
        y_empty = (getattr(Y, 'is_EmptySet', False) is True)
        
        # The product space is compact iff both X and Y are compact (or if it's empty)
        if x_empty or y_empty:
            prod_compact = True
        else:
            prod_compact = is_compact(X) and is_compact(Y)
            
        neg_q = not prod_compact
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (Y, d_Y) is a compact metric space",
    "H_2: X x Y is the Cartesian product space equipped with the product metric",
    "¬Q: The metric space X x Y is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2