import sympy
from sympy import S, Interval, Symbol, FiniteSet, Union, Intersection
from sympy import Reals, Rationals, Integers, Naturals

R = S.Reals
Q = S.Rationals
Z = S.Integers
N = S.Naturals

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], sympy.Set):
            X = witness[0]
        else:
            X = witness
    except Exception:
        X = witness

    try:
        if isinstance(X, sympy.Set):
            h1 = X.is_subset(S.Reals)
            if h1 is None:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(X, sympy.Set):
            closure = X.closure
            neg_q = (closure != X)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: There exists a Cauchy sequence in X that does not converge to a point in X"
]

N_HYP = 1
NEG_Q_INDEX = 1