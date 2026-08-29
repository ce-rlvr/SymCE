import sympy
from sympy import S

# Top-level setup
# (No specific named objects required for this real analysis theorem, 
# but we provide standard sympy tools just in case)

def conditions(witness) -> list[bool]:
    # Extract X if witness is a tuple (X, d)
    if isinstance(witness, tuple) and len(witness) == 2:
        X, d = witness
    else:
        X = witness

    # Convert list/set/tuple/scalar to a sympy FiniteSet for evaluation
    if isinstance(X, (list, set, frozenset, tuple)):
        try:
            X = sympy.FiniteSet(*X)
        except Exception:
            pass
    elif isinstance(X, (int, float)) or (isinstance(X, sympy.Basic) and not isinstance(X, sympy.Set)):
        try:
            X = sympy.FiniteSet(X)
        except Exception:
            pass

    # H_1: (X, d) is a non-empty compact metric space
    try:
        if not isinstance(X, sympy.Set):
            h1 = False
        elif X.is_empty is True:
            h1 = False
        elif X.is_subset(S.Reals) is not True:
            h1 = False
        else:
            # In R with the standard metric, compact is equivalent to closed and bounded
            is_bounded = (X.inf.is_finite is True) and (X.sup.is_finite is True)
            is_closed = (X.boundary.is_subset(X) is True)
            h1 = is_bounded and is_closed
    except Exception:
        h1 = False

    # neg_Q: The set X is NOT uncountable (i.e., X is countable or finite)
    try:
        if not isinstance(X, sympy.Set):
            neg_q = False
        else:
            neg_q = (X.is_countable is True) or (X.is_finite is True)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a non-empty compact metric space",
    "¬Q: The set X is not uncountable"
]

N_HYP = 1
NEG_Q_INDEX = 1