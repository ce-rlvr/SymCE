import sympy
from sympy import Piecewise, Interval

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        f, a, b = witness
        if isinstance(f, str):
            f_expr = sympy.sympify(f)
        elif callable(f):
            f_expr = f(x)
        else:
            f_expr = f
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]

    try:
        integral_val = sympy.integrate(f_expr, (x, a, b))
        try:
            h1 = abs(float(integral_val)) < 1e-12
        except TypeError:
            h1 = (sympy.simplify(integral_val) == 0)
    except Exception:
        h1 = False

    try:
        h2 = False
        for i in range(101):
            pt = a + (b - a) * sympy.Rational(i, 100)
            val = f_expr.subs(x, pt)
            try:
                if abs(float(val)) > 1e-12:
                    h2 = True
                    break
            except TypeError:
                if sympy.simplify(val) != 0:
                    h2 = True
                    break
    except Exception:
        h2 = False

    try:
        roots = sympy.solveset(f_expr, x, domain=sympy.Interval.open(a, b))
        if roots is sympy.EmptySet:
            neg_q = True
        elif isinstance(roots, sympy.FiniteSet) and len(roots) == 0:
            neg_q = True
        elif getattr(roots, 'is_empty', False) is True:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The definite integral of f from a to b equals 0",
    "H_2: f is not identically zero on the closed interval",
    "¬Q: There is no point c in the open interval such that f(c) equals 0"
]

N_HYP = 2
NEG_Q_INDEX = 2