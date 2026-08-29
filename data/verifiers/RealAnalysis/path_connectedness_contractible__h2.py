import sympy
from sympy import Interval, FiniteSet, ProductSet, Union, Set, S

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_not_path_connected(space):
    if space == S.EmptySet:
        return False
    if isinstance(space, Interval):
        return False
    if space == S.Reals:
        return False
    if space in (S.Integers, S.Naturals, S.Naturals0, S.Rationals):
        return True
    if isinstance(space, FiniteSet):
        return len(space) > 1
    if isinstance(space, ProductSet):
        return any(is_not_path_connected(factor) for factor in space.sets)
    if isinstance(space, Union):
        if space.is_subset(S.Reals) == True:
            return True
        raise ValueError("Cannot reliably determine path-connectedness for this Union")
    raise ValueError("Unknown set type")

def conditions(witness):
    try:
        h1 = isinstance(witness, Set)
    except Exception:
        h1 = False

    try:
        neg_q = is_not_path_connected(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "¬Q: X is not path-connected"
]

N_HYP = 1
NEG_Q_INDEX = 1