import sympy as sp
from sympy.abc import x
import math

CONDITION_LABELS = [
    "H_1: f is strictly monotonic",
    "¬Q: The inverse function is not continuous"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a dictionary with 'f', 'a', 'b', a tuple (f, a, b), or just f (defaulting to [0, 1]).
    """
    if isinstance(witness, dict):
        f_obj = witness.get('f', None)
        a = witness.get('a', 0.0)
        b = witness.get('b', 1.0)
    elif isinstance(witness, tuple) and len(witness) == 3:
        f_obj, a, b = witness
    else:
        f_obj = witness
        a, b = 0.0, 1.0
        
    try:
        a = float(a)
        b = float(b)
    except Exception:
        return [False, False]
        
    if f_obj is None:
        return [False, False]
        
    # Convert symbolic expressions to callable functions
    if hasattr(f_obj, 'free_symbols'):
        try:
            f = sp.lambdify(x, f_obj, modules=['math'])
            f(a)  # Test evaluation
        except Exception:
            def f(val):
                return float(f_obj.subs(x, val))
    elif callable(f_obj):
        f = f_obj
    else:
        return [False, False]
        
    # Evaluate H_1: f is strictly monotonic on [a,b]
    try:
        N = 1000
        pts = [a + i*(b-a)/N for i in range(N+1)]
        vals = [float(f(p)) for p in pts]
        
        diffs = [vals[i+1] - vals[i] for i in range(N)]
        
        strictly_increasing = all(d > 0 for d in diffs)
        strictly_decreasing = all(d < 0 for d in diffs)
        
        H1 = strictly_increasing or strictly_decreasing
    except Exception:
        H1 = False
        
    # Evaluate ¬Q: The inverse function f^{-1} is not continuous
    # The intended counterexample is a strictly monotonic function that is NOT continuous.
    # If f is not continuous, its image f([a,b]) has gaps, which in the context of this 
    # false conjecture is equated with f^{-1} being discontinuous.
    try:
        if H1:
            is_continuous = True
            # We check for jump discontinuities by looking for large local variations
            # that do not vanish when zooming in.
            for i in range(N):
                d = abs(diffs[i])
                if d > 1e-3:
                    sub_N = 100
                    sub_a = pts[i]
                    sub_b = pts[i+1]
                    sub_pts = [sub_a + j*(sub_b - sub_a)/sub_N for j in range(sub_N+1)]
                    sub_vals = [float(f(p)) for p in sub_pts]
                    sub_max_diff = max(abs(sub_vals[j+1] - sub_vals[j]) for j in range(sub_N))
                    
                    # If the maximum difference remains roughly the same after zooming in,
                    # it is a jump discontinuity rather than a steep continuous curve.
                    if sub_max_diff > 0.5 * d:
                        is_continuous = False
                        break
            neg_Q = not is_continuous
        else:
            neg_Q = False
    except Exception:
        neg_Q = False
        
    return [H1, neg_Q]