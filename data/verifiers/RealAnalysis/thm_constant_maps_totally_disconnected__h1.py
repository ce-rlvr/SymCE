import sympy
from sympy import FiniteSet, S, Expr, sympify
from sympy.abc import x
import math
import itertools
import functools

def evaluate_f(f, x_val):
    if isinstance(f, dict):
        return f[x_val]
    elif hasattr(f, '__call__'):
        return f(x_val)
    elif isinstance(f, Expr):
        free = list(f.free_symbols)
        if len(free) == 1:
            return f.subs(free[0], x_val)
        elif len(free) == 0:
            return f
    raise ValueError("Cannot evaluate f")

def conditions(witness):
    try:
        if isinstance(witness, dict):
            X = witness.get('X')
            Y = witness.get('Y')
            f = witness.get('f')
        else:
            X, Y, f = witness
    except Exception:
        return [False, False, False]

    # H1: Y is a totally disconnected topological space
    try:
        h1 = False
        if isinstance(Y, (set, frozenset, list, tuple)):
            h1 = True
        elif isinstance(Y, FiniteSet):
            h1 = True
        elif Y in [S.Integers, S.Naturals, S.Naturals0, S.Rationals]:
            h1 = True
    except Exception:
        h1 = False

    # H2: f: X \to Y is a continuous function
    # (For finite sets X, the subspace topology from R is discrete, so any function is continuous)
    try:
        h2 = False
        if isinstance(X, (set, frozenset, list, tuple, FiniteSet)):
            h2 = True
            for pt in X:
                val = evaluate_f(f, pt)
                if isinstance(Y, (set, frozenset, list, tuple)):
                    if not any(val == y for y in Y):
                        h2 = False
                        break
                else:
                    if Y.contains(sympify(val)) != S.true:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: The function f is not a constant function
    try:
        neg_q = False
        vals = []
        if isinstance(X, (set, frozenset, list, tuple, FiniteSet)):
            elements = list(X)
        else:
            elements = []
            
        for pt in elements:
            vals.append(evaluate_f(f, pt))
            
        if len(vals) > 1:
            first = vals[0]
            for v in vals[1:]:
                if v != first:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Y is a totally disconnected topological space",
    "H_2: f: X \\to Y is a continuous function",
    "¬Q: The function f is not a constant function"
]

N_HYP = 2
NEG_Q_INDEX = 2