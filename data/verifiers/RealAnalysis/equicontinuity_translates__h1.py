import sympy
from sympy.abc import x
import math

def conditions(witness):
    """
    Checks if the witness function is NOT uniformly continuous on R.
    Returns [True] if it is NOT uniformly continuous (conclusion fails),
    and [False] if it IS uniformly continuous.
    """
    if not isinstance(witness, sympy.Expr):
        return [False]
        
    free_symbols = witness.free_symbols
    if len(free_symbols) > 1:
        return [False]
    elif len(free_symbols) == 1:
        var = list(free_symbols)[0]
        f_expr = witness.subs(var, x)
    else:
        f_expr = witness

    # Attempt to lambdify for fast float64 evaluation
    try:
        f_math = sympy.lambdify(x, f_expr, modules=['math'])
        f_math(1.0)
        use_math = True
    except Exception:
        use_math = False

    # Compute symbolic derivative to detect catastrophic cancellation
    f_prime_expr = sympy.diff(f_expr, x)
    try:
        f_prime_math = sympy.lambdify(x, f_prime_expr, modules=['math'])
        f_prime_math(1.0)
        use_prime = True
    except Exception:
        use_prime = False

    def evaluate_diff(val, delta):
        if use_math:
            try:
                v_float = float(val)
                d_float = float(delta)
                
                # Check for input catastrophic cancellation (x + d == x in float64)
                if v_float + d_float == v_float:
                    if use_prime:
                        deriv = f_prime_math(v_float)
                        if abs(deriv) * d_float < 0.1:
                            return 0.0  # Difference is definitely small, skip evalf
                    # If derivative is large or unavailable, fallback to evalf
                else:
                    v1 = f_math(v_float)
                    v2 = f_math(v_float + d_float)
                    diff = abs(v2 - v1)
                    
                    # Check for output catastrophic cancellation
                    if use_prime:
                        deriv = f_prime_math(v_float)
                        expected_diff = abs(deriv) * d_float
                        if expected_diff >= 0.1:
                            # If v1 is so large that expected_diff is lost in float64 precision
                            if v1 + expected_diff == v1 or v2 - expected_diff == v2:
                                pass # Fallback to evalf
                            else:
                                return diff
                        else:
                            return diff
                    else:
                        return diff
            except Exception:
                pass # Fallback to evalf on overflow or domain errors
                
        # Fallback to 50-digit arbitrary precision evaluation
        try:
            v1 = f_expr.subs(x, val).evalf(50)
            v2 = f_expr.subs(x, val + delta).evalf(50)
            if hasattr(v1, 'is_real') and v1.is_real is False:
                return 0.0
            if hasattr(v2, 'is_real') and v2.is_real is False:
                return 0.0
            return float(abs(v2 - v1))
        except OverflowError:
            return float('inf')
        except Exception:
            return 0.0

    # Generate a robust set of test points covering magnitudes from 10^-20 to 10^50
    test_x = []
    for m in range(-20, 51):
        base = 10**m
        step = base * 0.137  # Pseudo-random phase sampling for periodic functions
        for j in range(50):
            val = base + j * step
            test_x.append(val)
            test_x.append(-val)

    # Test a sequence of decreasing deltas
    deltas = [10**(-k) for k in range(1, 21)]

    for delta in deltas:
        found = False
        for val in test_x:
            diff = evaluate_diff(val, delta)
            if diff > 0.5:
                found = True
                break
                
        if not found:
            # For this delta, no x gave a significant difference.
            # The function is likely uniformly continuous.
            return [False]
            
    # For all deltas, we found an x where the difference is > 0.5.
    # The function is NOT uniformly continuous.
    return [True]

CONDITION_LABELS = [
    "¬Q: The family of translated functions is not uniformly equicontinuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0