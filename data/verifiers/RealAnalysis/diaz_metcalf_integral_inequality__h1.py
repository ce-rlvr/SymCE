import sympy
from sympy import Symbol, Interval, solveset, diff, integrate
import math

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false Diaz-Metcalf Integral Inequality conjecture.
    The witness should be a dictionary or tuple providing f, g, a, b, m, M.
    """
    if isinstance(witness, dict):
        f = sympy.sympify(witness.get('f', 0))
        g = sympy.sympify(witness.get('g', 0))
        a = witness.get('a', 0)
        b = witness.get('b', 0)
        m = witness.get('m', 0)
        M = witness.get('M', 0)
    else:
        try:
            f, g, a, b, m, M = witness
            f = sympy.sympify(f)
            g = sympy.sympify(g)
        except Exception:
            return [False, False, False, False]

    # H1: a < b
    try:
        h1 = float(a) < float(b)
    except Exception:
        h1 = False

    # H2: g(x) != 0 for all x in a to b
    h2 = False
    try:
        if h1:
            n = 500
            h_step = (float(b) - float(a)) / n
            h2_ok = True
            for i in range(n + 1):
                val = complex(g.subs(x, float(a) + i * h_step).evalf())
                if abs(val) < 1e-7:
                    h2_ok = False
                    break
            
            if h2_ok:
                roots = solveset(g, x, domain=Interval(a, b))
                if roots.is_empty:
                    h2 = True
                elif roots.is_FiniteSet and len(roots) == 0:
                    h2 = True
                elif roots.is_FiniteSet and len(roots) > 0:
                    h2 = False
                else:
                    h2 = True
    except Exception:
        h2 = False

    # H3: m <= f(x)/g(x) <= M for all x in a to b
    h3 = False
    try:
        if h1 and h2:
            h_expr = f / g
            n = 500
            step = (float(b) - float(a)) / n
            h3_ok = True
            for i in range(n + 1):
                val = complex(h_expr.subs(x, float(a) + i * step).evalf())
                if abs(val.imag) > 1e-5:
                    h3_ok = False
                    break
                if val.real < float(m) - 1e-5 or val.real > float(M) + 1e-5:
                    h3_ok = False
                    break
            
            if h3_ok:
                crit_points = solveset(diff(h_expr, x), x, domain=Interval(a, b))
                points = {float(a), float(b)}
                if crit_points.is_FiniteSet:
                    for cp in crit_points:
                        points.add(float(cp.evalf()))
                
                h3_rigorous = True
                for p in points:
                    if p < float(a) - 1e-9 or p > float(b) + 1e-9:
                        continue
                    val = complex(h_expr.subs(x, p).evalf())
                    if abs(val.imag) > 1e-5:
                        h3_rigorous = False
                        break
                    if val.real < float(m) - 1e-5 or val.real > float(M) + 1e-5:
                        h3_rigorous = False
                        break
                h3 = h3_rigorous
    except Exception:
        h3 = False

    # neg_Q: \int_a^b f(x)^2 dx + mM \int_a^b g(x)^2 dx > (m+M) \int_a^b f(x)g(x) dx
    neg_Q = False
    try:
        if h1:
            def get_integral(expr):
                try:
                    res = integrate(expr, (x, a, b)).evalf()
                    if res.has(sympy.Integral):
                        raise ValueError("Unevaluated")
                    return complex(res)
                except Exception:
                    n_int = 500
                    h_int = (float(b) - float(a)) / n_int
                    tot = complex(expr.subs(x, float(a)).evalf()) + complex(expr.subs(x, float(b)).evalf())
                    for i in range(1, n_int, 2):
                        tot += 4 * complex(expr.subs(x, float(a) + i * h_int).evalf())
                    for i in range(2, n_int-1, 2):
                        tot += 2 * complex(expr.subs(x, float(a) + i * h_int).evalf())
                    return tot * h_int / 3

            int_f2 = get_integral(f**2)
            int_g2 = get_integral(g**2)
            int_fg = get_integral(f*g)
            
            LHS = int_f2 + float(m) * float(M) * int_g2
            RHS = (float(m) + float(M)) * int_fg
            
            if abs(LHS.imag) > 1e-5 or abs(RHS.imag) > 1e-5:
                neg_Q = True
            else:
                if LHS.real > RHS.real + 1e-5:
                    neg_Q = True
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = ['H_1: a < b', 'H_2: g(x) != 0 for all x in a to b', 'H_3: m <= f(x)/g(x) <= M for all x in a to b', 'neg_Q: Integral inequality fails']
N_HYP = 3
NEG_Q_INDEX = 3