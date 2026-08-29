import sympy
from sympy import integrate, Interval
from sympy.calculus.util import minimum
import math

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f', 0)
            g = witness.get('g', 0)
            a = witness.get('a', 0)
            b = witness.get('b', 0)
        else:
            f, g, a, b = witness
            
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = sympy.sympify(f)
            
        if callable(g):
            g_expr = g(x)
        else:
            g_expr = sympy.sympify(g)
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False]

    # H1: f(x) <= g(x) for all x in interval a to b
    h1_ok = False
    try:
        if float(a) > float(b):
            h1_ok = True
        else:
            diff = g_expr - f_expr
            try:
                m = minimum(diff, x, Interval(a, b))
                try:
                    h1_ok = bool(m >= 0)
                except TypeError:
                    h1_ok = bool(m.evalf() >= 0)
            except Exception:
                h1_ok = True
                a_f = float(a)
                b_f = float(b)
                for i in range(101):
                    pt = a_f + (b_f - a_f) * i / 100.0
                    val = diff.subs(x, pt).evalf()
                    if val < -1e-7:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # neg_Q: \int_a^b f(x) dx > \int_a^b g(x) dx
    neg_q_ok = False
    try:
        int_f = integrate(f_expr, (x, a, b))
        int_g = integrate(g_expr, (x, a, b))
        
        diff_int = int_f - int_g
        try:
            neg_q_ok = bool(diff_int > 0)
        except TypeError:
            neg_q_ok = bool(diff_int.evalf() > 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ['H_1: f(x) <= g(x) for all x in interval a to b', 'not Q: integral of f from a to b > integral of g from a to b']

N_HYP = 1
NEG_Q_INDEX = 1