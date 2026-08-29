import sympy
from sympy import Interval, FiniteSet, Reals, Union, Intersection, EmptySet
from sympy.sets.sets import Set

R = Reals

def is_connected_real_set(S):
    if isinstance(S, Interval):
        return True
    if isinstance(S, FiniteSet) and len(S) <= 1:
        return True
    if S == Reals:
        return True
    if S == EmptySet:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        iterator = iter(witness)
        collection = list(iterator)
        h1 = len(collection) > 0 and all(isinstance(s, Set) for s in collection)
    except Exception:
        h1 = False
        collection = []

    try:
        h2 = h1 and all(is_connected_real_set(s) for s in collection)
    except Exception:
        h2 = False

    try:
        if h1:
            union_set = Union(*collection)
            neg_q = not is_connected_real_set(union_set)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a topological space and {A_i} is a collection of subsets of X",
    "H_2: {A_i} is a collection of connected subsets of X",
    "¬Q: The union ∪ A_i for all i in the collection is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2