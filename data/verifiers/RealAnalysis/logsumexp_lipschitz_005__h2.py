import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
# No specific named bindings are required for this real analysis conjecture,
# but standard symbols are available if the witness uses them.

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the hypothesis and violates the conclusion.
    The witness can be the dimension `n` (e.g., n=0 where the function is not real-valued),
    or a pair of points (x, y) in R^n that violates the Lipschitz condition.
    """
    try:
        # Check if witness is just the dimension n
        if isinstance(witness, int):
            n = witness
            h1 = True
            # If n=0, f(x) = log(0) = -inf, which is not in R, so it cannot be globally Lipschitz.
            neg_q = (n == 0)
            return [h1, neg_q]
            
        # Check if witness is a tuple (n, x, y)
        if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
            n, x_val, y_val = witness
        # Check if witness is a tuple (x, y)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            x_val, y_val = witness
            if not isinstance(x_val, (tuple, list)) or not isinstance(y_val, (tuple, list)):
                return [False, False]
            n = len(x_val)
        else:
            return [False, False]
            
        if len(x_val) != n or len(y_val) != n:
            return [False, False]
            
        try:
            x_val = [float(xi) for xi in x_val]
            y_val = [float(yi) for yi in y_val]
            h1 = True
        except Exception:
            return [False, False]
            
        if n == 0:
            return [h1, True]
            
        def logsumexp(v):
            m = max(v)
            return m + math.log(sum(math.exp(vi - m) for vi in v))
            
        fx = logsumexp(x_val)
        fy = logsumexp(y_val)
        
        diff_f = abs(fx - fy)
        norm_inf = max(abs(xi - yi) for xi, yi in zip(x_val, y_val))
        
        # neg_Q: The function is NOT globally Lipschitz continuous with L=1.
        # This means there exist x, y such that |f(x) - f(y)| > ||x - y||_inf.
        # We use a small tolerance to avoid false positives from floating point rounding.
        neg_q = diff_f > norm_inf + 1e-9
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f is the LogSumExp function from R^n to R",
    "¬Q: f is NOT globally Lipschitz continuous with respect to the supremum norm with a Lipschitz constant of 1"
]

N_HYP = 1
NEG_Q_INDEX = 1