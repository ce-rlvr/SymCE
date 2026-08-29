import sympy
from sympy import Interval, oo
from sympy.calculus.util import continuous_domain
import math

# Top-level setup for default symbols
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If [a, b] is a closed and bounded interval in R, then f is absolutely continuous on [a, b]."
    """
    try:
        if isinstance(witness, dict):
            f = witness['f']
            x_sym = witness.get('x', x)
            a = witness['a']
            b = witness['b']
        else:
            if len(witness) == 4:
                f, x_sym, a, b = witness
            elif len(witness) == 3:
                f, a, b = witness
                x_sym = x
            else:
                return [False, False]
                
        if callable(f):
            f = f(x_sym)
    except Exception:
        return [False, False]
        
    # H_1: [a, b] is a closed and bounded interval in R
    h1 = False
    try:
        a_val = float(a)
        b_val = float(b)
        if a_val < b_val and math.isfinite(a_val) and math.isfinite(b_val):
            h1 = True
    except Exception:
        pass
        
    # neg_Q: f is NOT absolutely continuous on [a, b]
    neg_q = False
    
    # Check 1: Is it continuous on [a, b]?
    try:
        domain = continuous_domain(f, x_sym, Interval(a, b))
        if domain != Interval(a, b):
            neg_q = True
    except Exception:
        pass
        
    # Check 2: Numerical evaluation for discontinuities, infinities, or infinite variation
    if not neg_q:
        try:
            a_val = float(a)
            b_val = float(b)
            f_lam = sympy.lambdify(x_sym, f, modules=['math'])
            
            def get_variation_and_max_step(N):
                var = 0.0
                max_step = 0.0
                dx = (b_val - a_val) / N
                try:
                    prev_val = f_lam(a_val)
                except Exception:
                    prev_val = f_lam(a_val + dx/2)
                for i in range(1, N + 1):
                    x_curr = a_val + i * dx
                    try:
                        val = f_lam(x_curr)
                        if not math.isfinite(val):
                            return float('inf'), float('inf')
                        step = abs(val - prev_val)
                        var += step
                        if step > max_step:
                            max_step = step
                        prev_val = val
                    except Exception:
                        pass
                return var, max_step

            var_100, max_step_100 = get_variation_and_max_step(100)
            var_1000, max_step_1000 = get_variation_and_max_step(1000)
            var_10000, max_step_10000 = get_variation_and_max_step(10000)
            
            if var_10000 == float('inf'):
                neg_q = True
            elif var_10000 > 1e-7 and var_10000 > var_1000 * 1.1 and var_1000 > var_100 * 1.1:
                # Infinite variation (e.g. x * sin(1/x))
                neg_q = True
            elif max_step_10000 > 1e-3 and max_step_10000 > max_step_100 * 0.95:
                # Jump discontinuity
                neg_q = True
                
        except Exception:
            pass
            
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: the interval from a to b is closed and bounded in R",
    "¬Q: the function f is not absolutely continuous on the interval"
]

N_HYP = 1
NEG_Q_INDEX = 1