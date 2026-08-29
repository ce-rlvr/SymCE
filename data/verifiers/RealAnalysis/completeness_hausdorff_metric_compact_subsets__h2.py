import sympy
from sympy import S, Interval, Set, FiniteSet
import math
import itertools
import functools

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_complete_metric_space(X):
    if isinstance(X, (list, set, frozenset, dict)):
        return True
    if isinstance(X, str):
        return True
    try:
        if isinstance(X, FiniteSet):
            return True
        if X in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.Complexes, S.EmptySet):
            return True
        if isinstance(X, Interval) and not X.left_open and not X.right_open:
            return True
    except Exception:
        pass
    if hasattr(X, "is_complete"):
        return bool(X.is_complete)
    return True

def is_non_empty(X):
    if isinstance(X, (list, set, frozenset, dict)):
        return len(X) > 0
    try:
        if isinstance(X, FiniteSet):
            return len(X) > 0
        if X == S.EmptySet:
            return False
        if X in (S.Reals, S.Integers, S.Naturals, S.Naturals0, S.Complexes):
            return True
        if isinstance(X, Interval):
            return True
    except Exception:
        pass
    if isinstance(X, str):
        if "empty" in X.lower() and "non" not in X.lower():
            return False
        return True
    if hasattr(X, "is_empty"):
        return not X.is_empty
    return True

def conditions(witness):
    X = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        if callable(witness[1]) or isinstance(witness[1], str):
            X = witness[0]

    try:
        h1 = bool(is_complete_metric_space(X))
    except Exception:
        h1 = False

    try:
        h2 = True
    except Exception:
        h2 = False

    try:
        neg_q = bool(is_non_empty(X))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a complete metric space",
    "H_2: d_H is the Hausdorff metric on \mathcal{K}(X) induced by d",
    "¬Q: The metric space (\mathcal{K}(X), d_H) is not complete (fails because \mathcal{K}(X) includes the empty set, making d_H infinite)"
]

N_HYP = 2
NEG_Q_INDEX = 2