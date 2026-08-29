import sympy as sp
from sympy.abc import x, y, z, t

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = sp.sympify(witness['f'])
            g = sp.sympify(witness['g'])
            var = sp.sympify(witness['x'])
            a = sp.sympify(witness['a'])
            b = sp.sympify(witness['b'])
            m = sp.sympify(witness['m'])
            M = sp.sympify(witness['M'])
            p = sp.sympify(witness['p'])
            P = sp.sympify(witness['P'])
        else:
            f, g, var, a, b, m, M, p, P = witness
            f = sp.sympify(f)
            g = sp.sympify(g)
            var = sp.sympify(var)
            a = sp.sympify(a)
            b = sp.sympify(b)
            m = sp.sympify(m)
            M = sp.sympify(M)
            p = sp.sympify(p)
            P = sp.sympify(P)
    except Exception:
        return [False, False]

    def check_bounds(expr, v, a_val, b_val, lower, upper):
        try:
            if bool(a_val > b_val):
                return True
            if bool(a_val == b_val):
                val = expr.subs(v, a_val)
                return bool(lower <= val) and bool(val <= upper)
        except TypeError:
            pass
        
        try:
            if sp.simplify(expr).is_constant(v):
                val = expr.subs(v, a_val)
                return bool(lower <= val) and bool(val <= upper)
        except Exception:
            pass

        try:
            a_f = float(a_val)
            b_f = float(b_val)
            num_pts = [a_f + (b_f - a_f) * i / 50.0 for i in range(51)]
            num_vals = [float(expr.subs(v, pt)) for pt in num_pts]
            tol = 1e-5
            if not (bool(float(lower) <= min(num_vals) + tol) and bool(max(num_vals) - tol <= float(upper))):
                return False
        except Exception:
            pass

        try:
            min_val = sp.calculus.util.minimum(expr, v, sp.Interval(a_val, b_val))
            max_val = sp.calculus.util.maximum(expr, v, sp.Interval(a_val, b_val))
            return bool(lower <= min_val) and bool(max_val <= upper)
        except Exception:
            pass
        
        try:
            deriv = sp.diff(expr, v)
            crit_points = sp.solve(deriv, v)
            pts = [a_val, b_val]
            for cp in crit_points:
                if cp.is_real and a_val <= cp <= b_val:
                    pts.append(cp)
            vals = [expr.subs(v, pt) for pt in pts]
            return bool(lower <= min(vals)) and bool(max(vals) <= upper)
        except Exception:
            return False

    try:
        h1_f = check_bounds(f, var, a, b, m, M)
        h1_g = check_bounds(g, var, a, b, p, P)
        h1_ok = h1_f and h1_g
    except Exception:
        h1_ok = False

    try:
        if bool(a == b):
            neg_Q_ok = True
        else:
            int_fg = sp.integrate(f * g, (var, a, b))
            int_f = sp.integrate(f, (var, a, b))
            int_g = sp.integrate(g, (var, a, b))
            
            term1 = int_fg / (b - a)
            term2 = (int_f / (b - a)) * (int_g / (b - a))
            
            LHS = sp.Abs(term1 - term2)
            RHS = sp.Rational(1, 4) * (M - m) * (P - p)
            
            diff = sp.simplify(LHS - RHS)
            try:
                if diff.is_number and diff.is_real:
                    try:
                        neg_Q_ok = bool(diff > 0)
                    except TypeError:
                        val = diff.evalf()
                        neg_Q_ok = bool(val > 1e-9)
                else:
                    val = diff.evalf()
                    neg_Q_ok = bool(val > 1e-9)
            except TypeError:
                neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [h1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: There exist real constants m, M, p, P such that m <= f(x) <= M and p <= g(x) <= P for all x in the interval",
    "¬Q: The Gruess inequality fails"
]

N_HYP = 1
NEG_Q_INDEX = 1