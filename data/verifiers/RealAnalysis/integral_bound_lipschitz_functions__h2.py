import sympy as sp
from sympy.abc import x
from sympy.calculus.util import maximum, minimum
from sympy import Interval, diff
import math

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        f, a, b, L = witness
    except Exception:
        return [False, False, False]
        
    # H1: f is a real-valued function defined on interval a to b
    try:
        if callable(f):
            f_sym = f(x)
        else:
            f_sym = sp.sympify(f)
            
        f_a = float(f_sym.subs(x, a))
        h1 = True
    except Exception:
        h1 = False

    # H2: L is the Lipschitz constant for f on interval a to b
    try:
        if float(a) <= float(b):
            domain = Interval(float(a), float(b))
            df = diff(f_sym, x)
            try:
                max_df = maximum(df, x, domain)
                min_df = minimum(df, x, domain)
                true_L = max(abs(float(max_df)), abs(float(min_df)))
            except Exception:
                # Fallback to sampling for functions where maximum/minimum fails
                xs = [float(a) + i*(float(b)-float(a))/1000 for i in range(1001)]
                true_L = 0.0
                for i in range(1000):
                    x1, x2 = xs[i], xs[i+1]
                    y1 = float(f_sym.subs(x, x1))
                    y2 = float(f_sym.subs(x, x2))
                    slope = abs(y2 - y1) / abs(x2 - x1)
                    if slope > true_L:
                        true_L = slope
            
            h2 = abs(float(L) - float(true_L)) < 1e-3
        else:
            # If a > b, the interval is empty.
            # The Lipschitz constant on an empty set is vacuously 0.
            h2 = (float(L) == 0.0)
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        a_sym = sp.sympify(a)
        b_sym = sp.sympify(b)
        integral_val = sp.integrate(f_sym, (x, a_sym, b_sym))
        
        lhs = abs(float(integral_val) - float(f_a) * (float(b) - float(a)))
        rhs = float(L) * (float(b) - float(a))**2 / 2.0
        
        # neg_Q is True if the bound is strictly violated
        neg_q = lhs > rhs + 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on interval a to b",
    "H_2: L is the Lipschitz constant for f on interval a to b",
    "not Q: The integral bound fails"
]

N_HYP = 2
NEG_Q_INDEX = 2