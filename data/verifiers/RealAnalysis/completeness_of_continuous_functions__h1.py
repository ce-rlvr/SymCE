import sympy
from sympy import Set, S, Interval, FiniteSet, Union, Intersection

# Top-level setup for witness expressions
R = S.Reals
Z = S.Integers
Q = S.Rationals
N = S.Naturals

def conditions(witness) -> list[bool]:
    # H_1: C(K, R) is the space of all continuous real-valued functions on K
    # We verify that the witness K is a valid domain (a subset of Reals).
    try:
        h1 = isinstance(witness, Set) and (witness.is_subset(S.Reals) == True)
    except Exception:
        h1 = False

    # H_2: C(K, R) is equipped with the supremum metric d(f, g) = sup_{x in K} |f(x) - g(x)|
    # This is a definitional hypothesis regarding the metric space structure.
    h2 = True

    # ¬Q: C(K, R) is NOT a complete metric space.
    # For a subset K of R, C(K, R) with the supremum metric is a complete metric space
    # if and only if K is compact (closed and bounded). If K is not compact, there exist 
    # unbounded continuous functions on K, meaning the supremum metric can take the value 
    # infinity, and thus it fails to even be a valid metric space (let alone a complete one).
    try:
        if witness.is_empty == True:
            neg_q = False
        else:
            inf_val = witness.inf
            sup_val = witness.sup
            is_bounded = (inf_val.is_real == True) and (sup_val.is_real == True)
            is_closed = (witness.boundary.is_subset(witness) == True)
            is_compact = is_bounded and is_closed
            neg_q = not is_compact
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: C(K, R) is the space of all continuous real-valued functions on K",
    "H_2: C(K, R) is equipped with the supremum metric d(f, g) = sup_{x in K} |f(x) - g(x)|",
    "¬Q: C(K, R) is not a complete metric space"
]

N_HYP = 2
NEG_Q_INDEX = 2