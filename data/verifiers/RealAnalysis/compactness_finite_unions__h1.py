import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection

def is_compact(s):
    try:
        if s.is_empty == True:
            return True
        if not s.is_subset(S.Reals):
            return False
        if getattr(s.inf, 'is_infinite', False) or getattr(s.sup, 'is_infinite', False):
            return False
        if not s.boundary.is_subset(s):
            return False
        return True
    except Exception:
        return False

def conditions(witness):
    # Extract collection if witness is of the form (n, collection)
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int) and isinstance(witness[1], (list, tuple)):
            collection = witness[1]
        else:
            collection = witness
    except Exception:
        collection = witness

    # H1: n is a positive integer
    try:
        h1 = isinstance(collection, (list, tuple)) and len(collection) >= 1
    except Exception:
        h1 = False

    # H2: K_1, K_2, ..., K_n is a finite collection of compact subsets of X
    try:
        h2 = isinstance(collection, (list, tuple)) and all(is_compact(s) for s in collection)
    except Exception:
        h2 = False

    # neg_Q: The union of K_1, K_2, ..., K_n is not a compact subset of X
    try:
        if isinstance(collection, (list, tuple)) and len(collection) >= 1:
            union_set = Union(*collection)
            neg_q = not is_compact(union_set)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: K_1, K_2, ..., K_n is a finite collection of compact subsets of X",
    "¬Q: The union of K_1, K_2, ..., K_n is not a compact subset of X"
]

N_HYP = 2
NEG_Q_INDEX = 2