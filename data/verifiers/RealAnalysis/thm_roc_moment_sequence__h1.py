import sympy as sp
from sympy.abc import x, n
import math

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "Radius of Convergence for Moment Sequence Coefficients"
    """
    # The witness can be a single function f(x) or a tuple (f(x), a_n)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            f, a = witness
        else:
            return [False, False, False]
    else:
        f = witness
        a = None

    # Support both callable functions and sympy expressions
    if callable(f):
        try:
            f_expr = f(x)
        except Exception:
            f_expr = f
    else:
        f_expr = f

    # H_1: f(x) > 0 for all x in (0,1)
    h1_ok = True
    try:
        # Sample points in (0,1) to verify strict positivity
        for i in range(1, 100):
            val = complex(f_expr.subs(x, i / 100.0).evalf())
            if abs(val.imag) > 1e-9:
                h1_ok = False
                break
            if val.real <= 0:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H_2: a_n = \int_0^1 x^n f(x) dx for all integers n >= 0
    h2_ok = True
    if a is not None:
        try:
            # Check the definition for the first few terms
            for i in range(2):
                integral_val = sp.integrate(x**i * f_expr, (x, 0, 1))
                a_val = a.subs(n, i) if hasattr(a, 'subs') else a(i)
                
                if integral_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    if not (hasattr(a_val, 'has') and a_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan)):
                        if not (isinstance(a_val, float) and math.isinf(a_val)):
                            h2_ok = False
                            break
                else:
                    diff = sp.simplify(integral_val - a_val)
                    if diff != 0:
                        diff_num = abs(complex(diff.evalf()))
                        if diff_num > 1e-7:
                            h2_ok = False
                            break
        except Exception:
            h2_ok = False

    # ¬Q: The radius of convergence of the power series is NOT exactly 1
    # (If a_n is finite for all n, R = 1. Thus R != 1 iff the integral diverges for some n)
    neg_q = False
    try:
        if a is not None:
            if hasattr(a, 'subs'):
                ratio = sp.limit(sp.Abs(a.subs(n, n) / a.subs(n, n+1)), n, sp.oo)
                if ratio != 1:
                    neg_q = True
            # Also check if any a_n is infinite
            for i in range(5):
                a_val = a.subs(n, i) if hasattr(a, 'subs') else a(i)
                if hasattr(a_val, 'has') and a_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    neg_q = True
                    break
                if isinstance(a_val, float) and math.isinf(a_val):
                    neg_q = True
                    break
        else:
            # If a is not given, a_n is defined by the integral.
            for i in range(2):
                integral_val = sp.integrate(x**i * f_expr, (x, 0, 1))
                if integral_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    neg_q = True
                    break
                elif isinstance(integral_val, sp.Integral):
                    # Heuristic for divergence if sympy returns an unevaluated Integral
                    integrand = x**i * f_expr
                    lim0 = sp.limit(integrand, x, 0)
                    lim1 = sp.limit(integrand, x, 1)
                    
                    if lim0 == sp.oo:
                        lim_val = sp.limit(x * integrand, x, 0)
                        if lim_val == sp.oo or (lim_val.is_real and lim_val > 0):
                            neg_q = True
                            break
                    if lim1 == sp.oo:
                        lim_val = sp.limit((1-x) * integrand, x, 1)
                        if lim_val == sp.oo or (lim_val.is_real and lim_val > 0):
                            neg_q = True
                            break
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) > 0 for all x in (0,1)",
    "H_2: a_n = \\int_0^1 x^n f(x) dx for all integers n >= 0",
    "¬Q: The radius of convergence of the power series is NOT exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2