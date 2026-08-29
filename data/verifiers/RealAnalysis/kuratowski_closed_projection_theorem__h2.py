import sympy
from sympy import S, Set

# Top-level setup
Reals = S.Reals
Integers = S.Integers
Rationals = S.Rationals
Complexes = S.Complexes
EmptySet = S.EmptySet

def conditions(witness) -> list[bool]:
    # Extract X if witness is provided as a tuple (X, d_X)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X = witness[0]
        else:
            X = witness
    except Exception:
        X = witness

    # H_1: (X, d_X) is a metric space.
    # We accept any subset of the Reals as a valid metric space with the standard Euclidean metric.
    try:
        h1 = isinstance(X, Set) and (X.is_subset(S.Reals) == True)
    except Exception:
        h1 = False

    # ¬Q: The metric space (X, d_X) is NOT compact.
    # By Heine-Borel, a subset of Reals is compact if and only if it is closed and bounded.
    try:
        if not isinstance(X, Set):
            neg_q = False
        elif X == S.EmptySet:
            compact = True
            neg_q = not compact
        else:
            inf_val = X.inf
            sup_val = X.sup
            bounded = (inf_val.is_finite == True) and (sup_val.is_finite == True)
            closed = (X.closure == X)
            compact = bounded and closed
            neg_q = not compact
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) is a metric space",
    "¬Q: The metric space (X, d_X) is not compact"
]

N_HYP = 1
NEG_Q_INDEX = 1