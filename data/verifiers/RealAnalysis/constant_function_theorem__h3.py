import sympy
from sympy.abc import x

def conditions(witness):
    try:
        f, a, b = witness
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]
        
    try:
        if float(a) >= float(b):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: continuous on the closed interval
    h1 = False
    try:
        from sympy.calculus.util import continuous_domain
        dom = continuous_domain(f, x, sympy.Interval(a, b))
        h1 = bool(dom == sympy.Interval(a, b))
    except Exception:
        try:
            if f.is_polynomial(x):
                h1 = True
            else:
                sings = sympy.singularities(f, x)
                if sings.is_empty:
                    h1 = True
                elif sings.intersect(sympy.Interval(a, b)).is_empty:
                    h1 = True
        except Exception:
            h1 = False

    # H2: differentiable on the open interval
    h2 = False
    try:
        from sympy.calculus.util import continuous_domain
        df = sympy.diff(f, x)
        dom = continuous_domain(df, x, sympy.Interval(a, b, left_open=True, right_open=True))
        h2 = bool(dom == sympy.Interval(a, b, left_open=True, right_open=True))
    except Exception:
        try:
            df = sympy.diff(f, x)
            if df.is_polynomial(x):
                h2 = True
            else:
                sings = sympy.singularities(df, x)
                if sings.is_empty:
                    h2 = True
                elif sings.intersect(sympy.Interval(a, b, left_open=True, right_open=True)).is_empty:
                    h2 = True
        except Exception:
            h2 = False

    # neg_Q: f is not constant
    neg_q = False
    try:
        df = sympy.diff(f, x)
        df_simplified = sympy.simplify(df)
        if df_simplified != 0:
            neg_q = True
        else:
            v1 = sympy.simplify(f.subs(x, a))
            v2 = sympy.simplify(f.subs(x, b))
            if v1 != v2:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the closed interval",
    "H_2: f is differentiable on the open interval",
    "¬Q: f is not constant"
]

N_HYP = 2
NEG_Q_INDEX = 2