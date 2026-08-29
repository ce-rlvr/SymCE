import sympy as sp

x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval 0 to 1",
    "H_2: c > 0",
    "H_3: f(0) > 0",
    "H_4: f(1) < c",
    "¬Q: There does not exist x in the open interval 0 to 1 such that f(x) = c*x"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        f, c = witness
    except Exception:
        return [False, False, False, False, False]
    
    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
        f_expr = sp.sympify(f_expr)
    except Exception:
        return [False, False, False, False, False]

    # H1: f is a real-valued function defined on the closed interval 0 to 1
    try:
        h1 = True
        if len(f_expr.free_symbols - {x}) > 0:
            h1 = False
        else:
            for val in [0, 0.25, 0.5, 0.75, 1]:
                res = f_expr.subs(x, val)
                if res.is_real is False or res.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: c > 0
    try:
        h2 = bool(c > 0)
    except Exception:
        h2 = False

    # H3: f(0) > 0
    try:
        h3 = bool(f_expr.subs(x, 0) > 0)
    except Exception:
        h3 = False

    # H4: f(1) < c
    try:
        h4 = bool(f_expr.subs(x, 1) < c)
    except Exception:
        h4 = False

    # neg_Q: There does NOT exist x in (0, 1) such that f(x) == c*x
    try:
        neg_q = True
        sols = sp.solveset(f_expr - c * x, x, domain=sp.Interval.open(0, 1))
        if sols is sp.EmptySet or getattr(sols, 'is_empty', False) is True:
            neg_q = True
        elif isinstance(sols, sp.FiniteSet):
            for sol in sols:
                try:
                    val = float(sol.evalf())
                    if 0 < val < 1:
                        neg_q = False
                        break
                except Exception:
                    pass
        else:
            sols2 = sp.solve(f_expr - c * x, x)
            for sol in sols2:
                try:
                    val = float(sol.evalf())
                    if 0 < val < 1:
                        neg_q = False
                        break
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]