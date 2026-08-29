import sympy
from sympy import Interval, oo
from sympy.calculus.util import maximum, minimum, continuous_domain
import math

CONDITION_LABELS = [
    "H_1: f is bounded on the interval",
    "H_2: F is the integral of f",
    "¬Q: F is not Lipschitz continuous"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = sympy.sympify(witness.get('f'))
            F = sympy.sympify(witness.get('F'))
            a = sympy.sympify(witness.get('a'))
            b = sympy.sympify(witness.get('b'))
            x = witness.get('x', sympy.Symbol('x'))
            t = witness.get('t', sympy.Symbol('t'))
        else:
            f = sympy.sympify(witness[0])
            F = sympy.sympify(witness[1])
            a = sympy.sympify(witness[2])
            b = sympy.sympify(witness[3])
            x = sympy.sympify(witness[4]) if len(witness) > 4 else sympy.Symbol('x')
            t = sympy.sympify(witness[5]) if len(witness) > 5 else sympy.Symbol('t')

        if isinstance(x, str): x = sympy.Symbol(x)
        if isinstance(t, str): t = sympy.Symbol(t)
    except Exception:
        return [False, False, False]

    # H1: f is bounded on the interval
    h1_ok = False
    try:
        domain = Interval(a, b)
        max_val = maximum(f, t, domain)
        min_val = minimum(f, t, domain)
        if max_val < oo and min_val > -oo:
            h1_ok = True
        elif max_val == oo or min_val == -oo:
            h1_ok = False
        else:
            raise ValueError("Could not determine")
    except Exception:
        try:
            h1_ok = True
            if float(a) == float(b):
                pts = [float(a)]
            else:
                pts = [float(a) + i * (float(b) - float(a)) / 199 for i in range(200)]
            for pt in pts:
                v = f.subs(t, pt).evalf()
                if v == sympy.nan:
                    v = sympy.limit(f, t, pt).evalf()
                try:
                    v_float = float(v)
                    if abs(v_float) > 1e6:
                        h1_ok = False
                        break
                except TypeError:
                    h1_ok = False
                    break
        except Exception:
            h1_ok = False

    # H2: F(x) = integral of f(t) dt from a to x
    h2_ok = False
    try:
        val_a = F.subs(x, a).evalf()
        if abs(float(val_a)) < 1e-7:
            diff_F = sympy.diff(F, x)
            if sympy.simplify(diff_F - f.subs(t, x)) == 0 and not F.has(sympy.Piecewise):
                h2_ok = True
            else:
                match = True
                if float(a) == float(b):
                    pts = [float(a)]
                else:
                    pts = [float(a) + i * (float(b) - float(a)) / 6 for i in range(1, 6)]
                for val in pts:
                    F_val = F.subs(x, val).evalf()
                    int_val = sympy.Integral(f, (t, a, val)).evalf()
                    try:
                        if abs(float(F_val) - float(int_val)) > 1e-3:
                            match = False
                            break
                    except TypeError:
                        match = False
                        break
                if match:
                    h2_ok = True
    except Exception:
        pass

    # neg_Q: F is NOT Lipschitz continuous on the interval
    neg_q_ok = False
    try:
        domain = Interval(a, b)
        cont_dom = continuous_domain(F, x, domain)
        if cont_dom != domain:
            neg_q_ok = True
    except Exception:
        pass

    if not neg_q_ok:
        try:
            diff_F = sympy.diff(F, x)
            domain = Interval(a, b)
            max_val = maximum(diff_F, x, domain)
            min_val = minimum(diff_F, x, domain)
            if max_val == oo or min_val == -oo:
                neg_q_ok = True
            elif max_val < oo and min_val > -oo:
                neg_q_ok = False
            else:
                raise ValueError("Could not determine")
        except Exception:
            try:
                is_unbounded = False
                if float(a) == float(b):
                    pts = [float(a)]
                else:
                    pts = [float(a) + i * (float(b) - float(a)) / 199 for i in range(200)]
                for pt in pts:
                    v = diff_F.subs(x, pt).evalf()
                    if v == sympy.nan:
                        v = sympy.limit(diff_F, x, pt).evalf()
                    try:
                        v_float = float(v)
                        if abs(v_float) > 1e6:
                            is_unbounded = True
                            break
                    except TypeError:
                        is_unbounded = True
                        break
                if is_unbounded:
                    neg_q_ok = True
            except Exception:
                pass

    return [h1_ok, h2_ok, neg_q_ok]