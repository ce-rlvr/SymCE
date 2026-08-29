import math
import random
from sympy import Symbol, lambdify, S, diff, limit, oo, degree
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness function is NOT uniformly continuous on R.
    Returns [neg_Q] where neg_Q is True if the function fails to be uniformly continuous.
    """
    # 0. Quick numerical check for domain issues (e.g., singularities, complex values)
    try:
        f_test = lambdify(x, witness, modules=['math', 'numpy'])
        failures = 0
        for val in [-12.34, -1.23, 0, 1.23, 12.34]:
            try:
                y = float(f_test(val))
                if math.isnan(y) or math.isinf(y):
                    failures += 1
            except Exception:
                failures += 1
        if failures > 0:
            return [True]
    except Exception:
        pass

    # 1. Check continuity on R using sympy
    try:
        dom = continuous_domain(witness, x, S.Reals)
        if dom != S.Reals:
            return [True]
    except Exception:
        pass

    # 2. Check if it's a polynomial
    try:
        if witness.is_polynomial(x):
            deg = degree(witness, x)
            if deg > 1:
                return [True]
            else:
                return [False]
    except Exception:
        pass

    # 3. Check limits at +/- infinity
    try:
        lim_inf = limit(witness, x, oo)
        lim_ninf = limit(witness, x, -oo)
        if lim_inf.is_real and lim_ninf.is_real:
            # Both limits are finite, so it's bounded and continuous -> uniformly continuous
            return [False]
    except Exception:
        pass

    # 4. Check derivative limits for unbounded growth
    try:
        deriv_expr = diff(witness, x)
        try:
            lim_d_inf = limit(deriv_expr, x, oo)
            if abs(lim_d_inf) == oo:
                return [True]
        except Exception:
            pass
            
        try:
            lim_d_ninf = limit(deriv_expr, x, -oo)
            if abs(lim_d_ninf) == oo:
                return [True]
        except Exception:
            pass
    except Exception:
        deriv_expr = None

    # 5. Numerical derivative growth check for oscillating or complex functions
    try:
        if deriv_expr is not None:
            deriv_f = lambdify(x, deriv_expr, modules=['math', 'numpy'])
            def get_d(val):
                try:
                    res = abs(deriv_f(val))
                    if math.isinf(res) or math.isnan(res):
                        return 1e300
                    return float(res)
                except Exception:
                    return 0.0
        else:
            f_num = lambdify(x, witness, modules=['math', 'numpy'])
            def get_d(val):
                try:
                    res = abs(f_num(val + 0.001) - f_num(val - 0.001)) / 0.002
                    if math.isinf(res) or math.isnan(res):
                        return 1e300
                    return float(res)
                except Exception:
                    return 0.0

        random.seed(42)
        
        max_d_small = 0.0
        for _ in range(1000):
            val = random.uniform(10, 100)
            d = get_d(val)
            if d > max_d_small: max_d_small = d
            
        max_d_large = 0.0
        for _ in range(1000):
            val = random.uniform(10000, 100000)
            d = get_d(val)
            if d > max_d_large: max_d_large = d
            
        max_d_huge = 0.0
        for _ in range(1000):
            val = random.uniform(1000000, 10000000)
            d = get_d(val)
            if d > max_d_huge: max_d_huge = d
            
        if max_d_huge > 1e100 or max_d_large > 1e100:
            return [True]
            
        # If the derivative is consistently growing across scales, it's unbounded
        if max_d_huge > max_d_large * 1.2 and max_d_large > max_d_small * 1.2 and max_d_huge > 10:
            return [True]
        else:
            return [False]
            
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: f is not uniformly continuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0