import sympy
from sympy import S, Set, Interval, FiniteSet, Union, Intersection

# Top-level setup for the namespace
R = S.Reals

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (A, B) of sympy Sets, checks if it is a valid counterexample
    to the conjecture.
    """
    # H_1: (X, d) is a metric space
    # We restrict our verifier to the real line with standard distance.
    try:
        A, B = witness
        h1 = (isinstance(A, Set) and isinstance(B, Set) and 
              (A.is_subset(S.Reals) == True) and (B.is_subset(S.Reals) == True))
    except Exception:
        h1 = False

    # H_2: A is a non-empty sequentially compact subset of X
    # In R, sequential compactness is equivalent to being closed and bounded.
    try:
        A, B = witness
        is_non_empty = (A.is_empty == False)
        is_bounded = (A.inf.is_finite == True) and (A.sup.is_finite == True)
        is_closed = (A.closure == A)
        h2 = bool(is_non_empty and is_bounded and is_closed)
    except Exception:
        h2 = False

    # H_3: A and B are disjoint
    try:
        A, B = witness
        h3 = bool(A.intersect(B).is_empty == True)
    except Exception:
        h3 = False

    # ¬Q: The distance between A and B is NOT strictly greater than zero (i.e., d(A,B) == 0)
    # Since A is compact, d(A, B) == 0 if and only if A intersects the closure of B.
    try:
        A, B = witness
        neg_q = bool(A.intersect(B.closure).is_empty == False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space (witnesses must be subsets of R)",
    "H_2: A is a non-empty sequentially compact subset of X",
    "H_3: A and B are disjoint",
    "¬Q: The distance between A and B is not strictly greater than zero"
]

N_HYP = 3
NEG_Q_INDEX = 3