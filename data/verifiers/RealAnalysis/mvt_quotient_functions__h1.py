import sympy
from sympy import Symbol, Interval, solveset, Eq, S, Piecewise
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f and g are differentiable on open interval a to b",
    "H_2: g(x) != 0 for all x in closed interval a to b",
    "H_3: a < b",
    "not Q: conclusion fails"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, g, a, b = witness
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False, False]

    # H1: f and g are differentiable on (a, b)
    try:
        df = f.diff(x)
        dg = g.diff(x)
        open_int = Interval.open(a, b)
        dom_df = continuous_domain(df, x, open_int)
        dom_dg = continuous_domain(dg, x, open_int)
        h1 = bool(open_int.is_subset(dom_df) and open_int.is_subset(dom_dg))
    except Exception:
        h1 = False

    # H2: g(x) != 0 for all x in closed interval a to b
    try:
        closed_int = Interval(a, b)
        zeros_g = solveset(g, x, domain=closed_int)
        if zeros_g.is_empty == True:
            h2 = True
        elif zeros_g.is_empty == False:
            h2 = False
        else:
            # Numerical fallback
            h2 = True
            a_f = float(a)
            b_f = float(b)
            for i in range(101):
                val = a_f + (b_f - a_f) * i / 100.0
                if abs(float(g.subs(x, val).evalf())) < 1e-9:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H3: a < b
    try:
        h3 = bool(a < b)
    except Exception:
        h3 = False

    # Negated Conclusion:
    try:
        LHS_exact = f.subs(x, b)/g.subs(x, b) - f.subs(x, a)/g.subs(x, a)
        RHS_expr = (df*g - f*dg) / (g**2) * (b - a)
        
        sols = solveset(Eq(RHS_expr, LHS_exact), x, domain=open_int)
        if sols.is_empty == True:
            neg_q = True
        elif sols.is_empty == False:
            neg_q = False
        else:
            # Numerical fallback with sign change detection
            LHS_val = float(LHS_exact.evalf())
            neg_q = True
            prev_diff = None
            a_f = float(a)
            b_f = float(b)
            for i in range(1, 1000):
                val = a_f + (b_f - a_f) * i / 1000.0
                try:
                    rhs_val = float(RHS_expr.subs(x, val).evalf())
                    diff = rhs_val - LHS_val
                    if abs(diff) < 1e-5:
                        neg_q = False
                        break
                    if prev_diff is not None and prev_diff * diff < 0:
                        neg_q = False
                        break
                    prev_diff = diff
                except Exception:
                    prev_diff = None
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]