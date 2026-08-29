import sympy as sp

# Top-level setup
t, y = sp.symbols('t y')

CONDITION_LABELS = [
    "H_1: F satisfies a global Lipschitz condition with respect to its second variable",
    "H_2: y_0 is a fixed initial vector",
    "H_3: The sequence of functions y_n is defined recursively",
    "not Q: The sequence of Picard iterates y_n does not form an equicontinuous family on the interval"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        F = witness['F']
        a = witness['a']
        b = witness['b']
        y0 = witness['y0']
    except Exception:
        return [False, False, False, False]

    # H_1: F satisfies a global Lipschitz condition with respect to its second variable.
    try:
        dFdy = sp.diff(F, y)
        h1 = True
        if dFdy.has(y):
            lim_inf = sp.limit(dFdy, y, sp.oo)
            if lim_inf in [sp.oo, -sp.oo, sp.zoo]:
                h1 = False
            lim_ninf = sp.limit(dFdy, y, -sp.oo)
            if lim_ninf in [sp.oo, -sp.oo, sp.zoo]:
                h1 = False
        if h1:
            if a != -sp.oo:
                L_a = sp.limit(dFdy, t, a)
                if L_a in [sp.oo, -sp.oo, sp.zoo]:
                    h1 = False
            if b != sp.oo:
                L_b = sp.limit(dFdy, t, b)
                if L_b in [sp.oo, -sp.oo, sp.zoo]:
                    h1 = False
    except Exception:
        h1 = False

    # H_2: y_0 is a fixed initial vector.
    try:
        y0_expr = sp.sympify(y0)
        h2 = not y0_expr.has(t) and not y0_expr.has(y)
    except Exception:
        h2 = False

    # H_3: The sequence of functions y_n is defined recursively
    try:
        F_y0 = F.subs(y, y0)
        y1 = y0 + sp.integrate(F_y0, (t, a, t))
        h3 = True
        if y1.has(sp.Integral):
            h3 = False
        else:
            if a != -sp.oo:
                val_a = sp.limit(y1, t, a)
                if val_a in [sp.oo, -sp.oo, sp.zoo, sp.nan]:
                    h3 = False
            if b != sp.oo:
                val_b = sp.limit(y1, t, b)
                if val_b in [sp.oo, -sp.oo, sp.zoo, sp.nan]:
                    h3 = False
    except Exception:
        h3 = False

    # not Q: The sequence of Picard iterates y_n does not form an equicontinuous family on the interval.
    try:
        neg_q = False
        if b == sp.oo or a == -sp.oo:
            F_y0 = F.subs(y, y0)
            y1 = y0 + sp.integrate(F_y0, (t, a, t))
            dy1 = sp.diff(y1, t)
            
            def is_unbounded(expr, var, limit_point):
                try:
                    lim = sp.limit(expr, var, limit_point)
                    if lim in [sp.oo, -sp.oo, sp.zoo]:
                        return True
                except Exception:
                    pass
                return False

            if b == sp.oo and is_unbounded(dy1, t, sp.oo):
                neg_q = True
            elif a == -sp.oo and is_unbounded(dy1, t, -sp.oo):
                neg_q = True
            else:
                F_y1 = F.subs(y, y1)
                y2 = y0 + sp.integrate(F_y1, (t, a, t))
                dy2 = sp.diff(y2, t)
                if b == sp.oo and is_unbounded(dy2, t, sp.oo):
                    neg_q = True
                elif a == -sp.oo and is_unbounded(dy2, t, -sp.oo):
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]