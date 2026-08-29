import sympy
from sympy import Set, S, Interval, Union, Intersection, FiniteSet, EmptySet
from sympy.abc import x, y, z

# Top-level setup
R = S.Reals
Z = S.Integers
N = S.Naturals

def conditions(witness):
    try:
        # H_1: C is equipped with the subspace topology inherited from the standard topology on R.
        # In our context, this means C is a subset of the real numbers.
        h1 = isinstance(witness, Set) and witness.is_subset(S.Reals) == True
    except Exception:
        h1 = False

    try:
        # ¬Q: C is not totally disconnected.
        # A subset of R is totally disconnected if and only if it contains no non-degenerate intervals.
        # This is equivalent to its interior in R being empty.
        # Therefore, C is NOT totally disconnected iff its interior is NOT empty.
        neg_q = witness.interior.is_empty is False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: C is equipped with the subspace topology inherited from the standard topology on R",
    "¬Q: C is not totally disconnected"
]

N_HYP = 1
NEG_Q_INDEX = 1