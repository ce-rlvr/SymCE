import sympy
from sympy import Symbol, Piecewise, Interval, solveset, Eq, S

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness):
    try:
        f_expr, g_expr, a, b = witness
        
        if callable(f_expr):
            f_expr = f_expr(x)
        if callable(g_expr):
            g_expr = g_expr(x)
            
        f_expr = sympy.sympify(f_expr)
        g_expr = sympy.sympify(g_expr)
        a = float(a)
        b = float(b)
    except Exception:
        return [False, False, False]

    # Generate a robust set of test points
    try:
        critical_points = {a, b}
        for expr in (f_expr, g_expr):
            for rel in expr.atoms(sympy.Relational):
                if rel.lhs == x and rel.rhs.is_number:
                    critical_points.add(float(rel.rhs))
                elif rel.rhs == x and rel.lhs.is_number:
                    critical_points.add(float(rel.lhs))
                    
        pts = set()
        for i in range(101):
            pts.add(a + (b - a) * i / 100.0)
        for c in critical_points:
            if a <= c <= b:
                pts.add(c)
                if c - 1e-5 >= a: pts.add(c - 1e-5)
                if c + 1e-5 <= b: pts.add(c + 1e-5)
    except Exception:
        pts = [a, b, (a + b) / 2.0]

    # H1: f and g are real-valued functions defined on the closed interval
    try:
        h1 = (a < b)
        if h1:
            for p in pts:
                val_f = f_expr.subs(x, p).evalf()
                val_g = g_expr.subs(x, p).evalf()
                if val_f.is_real is not True or val_g.is_real is not True:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: For all x in the interval, f(x) != g(x)
    try:
        domain = Interval(a, b)
        sols = solveset(Eq(f_expr, g_expr), x, domain=domain)
        if sols == S.EmptySet:
            h2 = True
        else:
            # Fallback using function_range if solveset returns a ConditionSet
            try:
                from sympy.calculus.util import function_range
                frange = function_range(f_expr - g_expr, x, domain)
                if not frange.contains(0):
                    h2 = True
                else:
                    h2 = False
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # Neg_Q: Not (f > g for all x or f < g for all x)
    # Meaning f(x) - g(x) takes both strictly positive and strictly negative values on the interval
    try:
        has_pos = False
        has_neg = False
        for p in pts:
            val_expr = (f_expr - g_expr).subs(x, p).evalf()
            if val_expr.is_real is not True:
                continue
            val = float(val_expr)
            if val > 0:
                has_pos = True
            elif val < 0:
                has_neg = True
            if has_pos and has_neg:
                break
        neg_q = has_pos and has_neg
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are real-valued functions defined on the closed interval",
    "H_2: For all x in the interval, f(x) != g(x)",
    "not Q: f(x) - g(x) changes sign on the interval"
]

N_HYP = 2
NEG_Q_INDEX = 2