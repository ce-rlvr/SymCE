import math
import sympy
from sympy import symbols, Piecewise, Eq

# Top-level setup for witness expressions
x, n = symbols('x n')

def is_continuous(func, a, b, n_points=100):
    """
    Numerically checks if a 1D function is continuous on [a, b].
    It looks for jump discontinuities by evaluating the function on a grid
    and zooming in on large differences using binary search.
    """
    dx = (b - a) / n_points
    for i in range(n_points):
        x_val = a + i * dx
        x_next = min(b, a + (i + 1) * dx)
        try:
            y1 = float(func(x_val))
            y2 = float(func(x_next))
            if abs(y1 - y2) > 0.1:
                left = x_val
                right = x_next
                # Binary search to find the steepest jump
                for _ in range(30):
                    mid = (left + right) / 2.0
                    if abs(float(func(left)) - float(func(mid))) > abs(float(func(mid)) - float(func(right))):
                        right = mid
                    else:
                        left = mid
                # If the jump remains large over a microscopic interval, it's a discontinuity
                if abs(float(func(left)) - float(func(right))) > 0.05:
                    return False
        except Exception:
            return False
    return True

def conditions(witness):
    try:
        if 'a' in witness and 'b' in witness:
            a = float(witness['a'])
            b = float(witness['b'])
        elif 'domain' in witness:
            a = float(witness['domain'][0])
            b = float(witness['domain'][1])
        else:
            a, b = 0.0, 0.0

        if callable(witness.get('f_n')):
            f_n_raw = witness['f_n']
            f_n = lambda n_val, x_val: float(f_n_raw(n_val, x_val))
        elif 'f_n_expr' in witness and 'x' in witness and 'n' in witness:
            expr = witness['f_n_expr']
            x_sym = witness['x']
            n_sym = witness['n']
            f_n_lam = sympy.lambdify((n_sym, x_sym), expr, 'math')
            f_n = lambda n_val, x_val: float(f_n_lam(n_val, x_val))
        else:
            f_n = None
    except Exception:
        return [False, False, False, False]

    # H_1: (X, d) is a compact metric space
    try:
        h1 = (a < b) and math.isfinite(a) and math.isfinite(b)
    except Exception:
        h1 = False

    if not h1 or f_n is None:
        return [False, False, False, False]

    # H_2: (f_n) is a sequence of continuous functions from X to R
    try:
        h2 = True
        for n_val in [1, 2, 10, 100]:
            if not is_continuous(lambda x_val: f_n(n_val, x_val), a, b):
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: For every x \in X and n \in \mathbb{N}, f_n(x) \leq f_{n+1}(x)
    try:
        h3 = True
        n_points = 1000
        dx = (b - a) / n_points
        for n_val in [1, 2, 10, 50]:
            for i in range(n_points + 1):
                x_val = min(b, a + i * dx)
                if f_n(n_val, x_val) > f_n(n_val + 1, x_val) + 1e-7:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: The sequence (f_n) does NOT converge uniformly to f on X
    # We check this by verifying that the sequence is NOT uniformly Cauchy.
    # If it is uniformly Cauchy, the maximum difference between f_M and f_N should be very small.
    try:
        neg_q = False
        N = 1000
        M = 10000
        n_points = 10000
        dx = (b - a) / n_points
        max_diff = 0.0
        for i in range(n_points + 1):
            x_val = min(b, a + i * dx)
            try:
                diff = f_n(M, x_val) - f_n(N, x_val)
                if diff > max_diff:
                    max_diff = diff
            except Exception:
                pass
        
        if max_diff > 0.05:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a compact metric space",
    "H_2: (f_n) is a sequence of continuous functions from X to R",
    "H_3: For every x in X and n in N, f_n(x) <= f_{n+1}(x)",
    "¬Q: The sequence (f_n) does NOT converge uniformly to f on X"
]

N_HYP = 3
NEG_Q_INDEX = 3