import sympy
from sympy import Symbol, integrate, diff, Interval, maximum, minimum, Abs

x = Symbol('x', real=True)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            a = witness.get('a')
            b = witness.get('b')
            M1 = witness.get('M1')
            M2 = witness.get('M2')
        else:
            f, g, a, b, M1, M2 = witness
    except Exception:
        return [False, False, False]

    try:
        f_a = f.subs(x, a)
        g_a = g.subs(x, a)
        try:
            h1 = (float(f_a) == 0.0) and (float(g_a) == 0.0)
        except Exception:
            h1 = bool(sympy.simplify(f_a) == 0) and bool(sympy.simplify(g_a) == 0)
    except Exception:
        h1 = False

    try:
        try:
            m1_ok = float(M1) > 0.0
            m2_ok = float(M2) > 0.0
        except Exception:
            m1_ok = bool(M1 > 0)
            m2_ok = bool(M2 > 0)
            
        if not (m1_ok and m2_ok):
            h2 = False
        else:
            df = diff(f, x)
            dg = diff(g, x)
            
            def check_bound(expr, var, a, b, M):
                try:
                    if float(a) > float(b):
                        return True
                except Exception:
                    if bool(a > b):
                        return True
                try:
                    max_val = maximum(expr, var, Interval(a, b))
                    min_val = minimum(expr, var, Interval(a, b))
                    try:
                        return float(max_val) <= float(M) and float(min_val) >= -float(M)
                    except Exception:
                        return bool(max_val <= M) and bool(min_val >= -M)
                except Exception:
                    deriv = diff(expr, var)
                    crit_points = sympy.solve(deriv, var)
                    pts = [a, b]
                    for p in crit_points:
                        if p.is_real:
                            try:
                                if float(a) <= float(p) <= float(b):
                                    pts.append(p)
                            except Exception:
                                if bool(a <= p) and bool(p <= b):
                                    pts.append(p)
                    for p in pts:
                        val = expr.subs(var, p)
                        try:
                            if float(abs(val)) > float(M):
                                return False
                        except Exception:
                            if bool(abs(val) > M):
                                return False
                    return True

            h2 = check_bound(df, x, a, b, M1) and check_bound(dg, x, a, b, M2)
    except Exception:
        h2 = False

    try:
        integral_val = integrate(f * g, (x, a, b))
        lhs = Abs(integral_val)
        rhs = (M1 * M2 / 3) * (b - a)**3
        try:
            neg_q = float(lhs) > float(rhs)
        except Exception:
            neg_q = bool(sympy.simplify(lhs - rhs) > 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(a) = 0 and g(a) = 0",
    "H_2: M1, M2 > 0 and derivatives bounded",
    "not Q: integral bound fails"
]

N_HYP = 2
NEG_Q_INDEX = 2