import sympy
from sympy import S, Interval, oo, FiniteSet

# Top-level setup: named object bindings that the witness expression may reference.
Reals = S.Reals
Integers = S.Integers
Naturals = S.Naturals
Rationals = S.Rationals
Complexes = S.Complexes

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (X, A) representing the metric space X and its subset A,
    or just a set A (in which case X is implicitly assumed to be the Reals).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X, A = witness
        else:
            X = S.Reals
            A = witness
    except Exception:
        return [False, False, False]

    # H_1: (X, d) is a complete metric space
    try:
        # Assuming the standard metric on R, a subspace is complete iff it is closed.
        if X in (S.Reals, S.Integers, S.Naturals):
            h1_ok = True
        else:
            h1_ok = (X.is_subset(S.Reals) is True) and (X.is_closed is True)
    except Exception:
        h1_ok = False

    # H_2: A is a subset of X
    try:
        h2_ok = (A.is_subset(X) is True) or (A == X)
    except Exception:
        h2_ok = False

    # ¬Q: The closure of A in X is NOT a compact set
    try:
        # In R, a closed set is compact iff it is bounded.
        # Since X is closed in R (from H_1), the closure of A in X is closed in R.
        # Therefore, the closure of A in X is compact iff it is bounded.
        # The closure of A is bounded iff A itself is bounded.
        # Thus, the closure of A in X is NOT compact iff A is NOT bounded.
        if A in (S.Reals, S.Integers, S.Naturals):
            neg_q_ok = True
        else:
            neg_q_ok = (A.is_bounded is False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (X, d) is a complete metric space",
    "H_2: A is a subset of X",
    "¬Q: The closure of A in X is not a compact set"
]

N_HYP = 2
NEG_Q_INDEX = 2