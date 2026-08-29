import sympy
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: f is a function on the interval",
    "H_2: f is continuous on the interval",
    "not Q: The image set of f on the interval is not bounded"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        f_val, a_val, b_val = witness
    except Exception:
        return [False, False, False]
        
    # H1: f is a function on the interval
    try:
        h1 = False
        a = sympy.sympify(a_val)
        b = sympy.sympify(b_val)
        if bool(a < b):
            f_expr = sympy.sympify(f_val)
            free_vars = list(f_expr.free_symbols)
            if len(free_vars) <= 1:
                if len(free_vars) == 1:
                    f_expr = f_expr.subs(free_vars[0], x)
                h1 = True
    except Exception:
        h1 = False

    # H2: f is continuous on the interval
    try:
        h2 = False
        if h1:
            from sympy.calculus.util import continuous_domain
            domain = continuous_domain(f_expr, x, sympy.S.Reals)
            interval = sympy.Interval(a, b)
            if interval.is_subset(domain):
                h2 = True
            else:
                # Fallback for continuity check
                n, d = sympy.fraction(sympy.cancel(f_expr))
                if d == 1:
                    h2 = True
                else:
                    roots = sympy.solve(d, x)
                    h2 = True
                    for r in roots:
                        if r.is_real or r == sympy.oo or r == -sympy.oo:
                            if a <= r and r <= b:
                                h2 = False
                                break
    except Exception:
        h2 = False

    # neg_Q: f is not bounded on the interval
    try:
        neg_q = False
        if h1 and h2:
            interval = sympy.Interval(a, b)
            from sympy.calculus.util import function_range
            try:
                frange = function_range(f_expr, x, interval)
                if frange.sup == sympy.oo or frange.inf == -sympy.oo:
                    neg_q = True
            except Exception:
                # Fallback to limits at infinity
                if a == -sympy.oo:
                    L = sympy.limit(f_expr, x, -sympy.oo)
                    if L == sympy.oo or L == -sympy.oo:
                        neg_q = True
                    elif hasattr(L, 'max') and hasattr(L, 'min'):
                        if L.max == sympy.oo or L.min == -sympy.oo:
                            neg_q = True
                if b == sympy.oo:
                    L = sympy.limit(f_expr, x, sympy.oo)
                    if L == sympy.oo or L == -sympy.oo:
                        neg_q = True
                    elif hasattr(L, 'max') and hasattr(L, 'min'):
                        if L.max == sympy.oo or L.min == -sympy.oo:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]