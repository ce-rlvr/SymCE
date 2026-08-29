import math
import itertools
import functools
import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness):
    # H_1: X is a topological space
    try:
        X, T = witness
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        
        h1_ok = True
        if frozenset() not in T_sets or X_set not in T_sets:
            h1_ok = False
        else:
            for A in T_sets:
                for B in T_sets:
                    if A.intersection(B) not in T_sets:
                        h1_ok = False
                        break
                    if A.union(B) not in T_sets:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # neg_Q: X is not a connected space
    try:
        X, T = witness
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        
        neg_q = False
        for A in T_sets:
            if A != frozenset() and A != X_set:
                if (X_set - A) in T_sets:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "¬Q: X is not a connected space"
]

N_HYP = 1
NEG_Q_INDEX = 1