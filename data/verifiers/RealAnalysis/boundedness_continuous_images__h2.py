import sympy
from sympy import Symbol, S, FiniteSet, Interval, Union
from sympy.calculus.util import continuous_domain, function_range

x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

def conditions(witness) -> list[bool]:
    try:
        X_raw = witness.get('X')
        f_raw = witness.get('f')
        if X_raw is None or f_raw is None:
            return [False, False, False]
        
        if isinstance(X_raw, (list, tuple, set)):
            X = FiniteSet(*X_raw)
        else:
            X = X_raw
            
        f = sympy.sympify(f_raw)
    except Exception:
        return [False, False, False]

    try:
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = x
    except Exception:
        var = x

    # H1: X is a compact metric space
    try:
        is_closed = X.is_closed
        is_bounded = X.is_bounded
        if is_closed is None or is_bounded is None:
            h1 = False
        else:
            h1 = bool(is_closed and is_bounded)
    except Exception:
        h1 = False

    # H2: f is continuous on X
    try:
        domain = continuous_domain(f, var, S.Reals)
        is_subset = X.is_subset(domain)
        if is_subset is None:
            h2 = False
        else:
            h2 = bool(is_subset)
    except Exception:
        h2 = False

    # neg_Q: f(X) is not bounded
    try:
        if isinstance(X, FiniteSet):
            images = [f.subs(var, val) for val in X]
            is_bounded = all(val.is_finite for val in images)
            neg_q = not is_bounded
        else:
            frange = function_range(f, var, X)
            is_bounded = frange.is_bounded
            if is_bounded is None:
                neg_q = False
            else:
                neg_q = not bool(is_bounded)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: f: X -> Y is a continuous function",
    "¬Q: The image f(X) is not a bounded subset of Y"
]

N_HYP = 2
NEG_Q_INDEX = 2