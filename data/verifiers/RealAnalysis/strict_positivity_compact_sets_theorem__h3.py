import sympy
from sympy import Interval
from sympy.calculus.util import continuous_domain, minimum
from sympy.abc import x
import math

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness is expected to be a tuple: (f, a, b)
    where f is a sympy expression (the function), and a, b are real numbers for the interval.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        f, a, b = witness
    except Exception:
        return [False, False, False]

    # Determine the variable of the function
    try:
        if hasattr(f, 'free_symbols'):
            free_symbols = f.free_symbols
            if len(free_symbols) == 1:
                var = list(free_symbols)[0]
            elif len(free_symbols) == 0:
                var = x
            else:
                return [False, False, False]
        else:
            f = sympy.sympify(f)
            var = x
    except Exception:
        return [False, False, False]

    # H_1: f is a real-valued function defined on the closed interval
    try:
        h1 = float(a) < float(b)
        if h1:
            # Check if it evaluates to real numbers at the endpoints and midpoint
            v1 = float(f.subs(var, a))
            v2 = float(f.subs(var, b))
            v3 = float(f.subs(var, (a + b) / 2))
            if math.isnan(v1) or math.isnan(v2) or math.isnan(v3):
                h1 = False
    except Exception:
        h1 = False

    # H_2: f is continuous at every point in the interval
    try:
        domain = continuous_domain(f, var, Interval(a, b))
        h2 = bool(domain == Interval(a, b))
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist delta > 0 such that f(x) >= delta for all x in the interval
    # This is equivalent to saying the minimum of f(x) on the interval is <= 0.
    try:
        min_val = minimum(f, var, Interval(a, b))
        neg_q = float(min_val) <= 0.0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: f is a real-valued function defined on the closed interval", "H_2: f is continuous at every point in the interval", "not_Q: min f(x) <= 0 on the interval"]
N_HYP = 2
NEG_Q_INDEX = 2