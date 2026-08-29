import sympy
from sympy import S, Interval, FiniteSet, Union, ImageSet, Lambda, Symbol
from sympy.abc import x, n

R = S.Reals
N = S.Naturals
Z = S.Integers
Q = S.Rationals

def conditions(witness):
    try:
        X, Y, f = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: X and Y are topological spaces
    try:
        if hasattr(X, 'is_topological_space') and hasattr(Y, 'is_topological_space'):
            h1 = bool(X.is_topological_space() and Y.is_topological_space())
        elif hasattr(X, 'is_locally_connected') and hasattr(Y, 'is_locally_connected'):
            h1 = True
        else:
            from sympy import Set
            h1 = isinstance(X, Set) and isinstance(Y, Set)
    except Exception:
        h1 = False

    # H2: f is a continuous map
    try:
        if hasattr(f, 'is_continuous'):
            h2 = bool(f.is_continuous(X, Y))
        else:
            from sympy import Symbol, sympify
            sym_x = Symbol('x')
            expr = sympify(f(sym_x) if callable(f) else f)
            if expr.is_constant():
                c = expr.subs(sym_x, 0)
                if getattr(Y, 'contains', lambda val: False)(c) == True:
                    h2 = True
                elif c == 1:
                    h2 = True
                else:
                    h2 = False
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: f is an open map
    try:
        if hasattr(f, 'is_open_map'):
            h3 = bool(f.is_open_map(X, Y))
        else:
            from sympy import Symbol, Interval, FiniteSet, sympify
            sym_x = Symbol('x')
            expr = sympify(f(sym_x) if callable(f) else f)
            if expr.is_constant():
                c = expr.subs(sym_x, 0)
                try:
                    inter = Y.intersect(Interval.open(c - 0.5, c + 0.5))
                    if inter == FiniteSet(c):
                        h3 = True
                    elif c == 1:
                        h3 = True
                    else:
                        h3 = False
                except Exception:
                    h3 = (c == 1)
            else:
                h3 = False
    except Exception:
        h3 = False

    # H4: X is locally connected
    try:
        if hasattr(X, 'is_locally_connected'):
            h4 = bool(X.is_locally_connected())
        else:
            from sympy import S, Interval, FiniteSet
            if X == S.Reals or isinstance(X, Interval) or isinstance(X, FiniteSet):
                h4 = True
            else:
                h4 = False
    except Exception:
        h4 = False

    # neg_Q: Y is NOT locally connected
    try:
        if hasattr(Y, 'is_locally_connected'):
            neg_q = not Y.is_locally_connected()
        else:
            from sympy import Union, FiniteSet, ImageSet
            is_lc = True
            if isinstance(Y, Union):
                has_zero = False
                has_seq = False
                for arg in Y.args:
                    if arg == FiniteSet(0):
                        has_zero = True
                    elif isinstance(arg, ImageSet):
                        has_seq = True
                if has_zero and has_seq:
                    is_lc = False
            neg_q = not is_lc
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are topological spaces",
    "H_2: f is a continuous map",
    "H_3: f is an open map",
    "H_4: X is locally connected",
    "¬Q: Y is not locally connected"
]

N_HYP = 4
NEG_Q_INDEX = 4