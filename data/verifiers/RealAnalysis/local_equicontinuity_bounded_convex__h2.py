import sympy
from sympy.abc import x, n
import math

# Top-level setup
# x and n are imported from sympy.abc and available for witness expressions.

def conditions(witness):
    # H_1: (a,b) is an open interval in R
    try:
        a = float(witness['a'])
        b = float(witness['b'])
        h1 = a < b
    except Exception:
        h1 = False

    # H_2: F is uniformly bounded on (a,b)
    try:
        F = witness['F']
        F_lam = sympy.lambdify((n, x), F, modules=['math', 'sympy'])
        
        a_f = float(witness['a'])
        b_f = float(witness['b'])
        
        # Cap infinite intervals for grid generation
        if a_f == float('-inf'):
            a_f = -1000.0
        if b_f == float('inf'):
            b_f = 1000.0
            
        if a_f >= b_f:
            h2 = False
        else:
            # Low-discrepancy sequence for robust sampling
            phi = (math.sqrt(5) - 1) / 2
            grid = [a_f + ((i * phi) % 1.0) * (b_f - a_f) for i in range(1, 10001)]
            
            h2 = True
            max_val = 0.0
            eval_success = False
            for n_val in [1, 10, 100, 1000, 10000]:
                for x_val in grid:
                    try:
                        val = abs(float(F_lam(n_val, x_val)))
                        eval_success = True
                        if val > max_val:
                            max_val = val
                    except Exception:
                        pass
                if max_val > 10000.0:
                    h2 = False
                    break
            if not eval_success:
                h2 = False
    except Exception:
        h2 = False

    # H_3: [c,d] is a compact subinterval contained in (a,b)
    try:
        a_val = float(witness['a'])
        b_val = float(witness['b'])
        c = float(witness['c'])
        d = float(witness['d'])
        h3 = (c < d) and (a_val < c) and (d < b_val)
    except Exception:
        h3 = False

    # not Q: F is not uniformly equicontinuous on [c,d]
    try:
        F = witness['F']
        F_lam = sympy.lambdify((n, x), F, modules=['math', 'sympy'])
        c = float(witness['c'])
        d = float(witness['d'])
        
        if c >= d:
            neg_q = False
        else:
            deltas = [1e-2, 1e-3, 1e-4, 1e-5]
            n_values = [1, 10, 100, 1000, 10000, 100000]
            
            phi = (math.sqrt(5) - 1) / 2
            grid = [c + ((i * phi) % 1.0) * (d - c) for i in range(1, 5001)]
            grid.extend([0.0, c, d, (c+d)/2])
            
            neg_q = True
            for delta in deltas:
                found_for_delta = False
                for n_val in n_values:
                    for x_val in grid:
                        if x_val + delta > d:
                            continue
                        try:
                            val1 = float(F_lam(n_val, x_val))
                            val2 = float(F_lam(n_val, x_val + delta))
                            if abs(val1 - val2) > 0.1:
                                found_for_delta = True
                                break
                        except Exception:
                            pass
                    if found_for_delta:
                        break
                # If for some delta we cannot find a violation, it might be equicontinuous
                if not found_for_delta:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b is an open interval in R",
    "H_2: F is uniformly bounded on a, b",
    "H_3: c, d is a compact subinterval contained in a, b",
    "not Q: F is not uniformly equicontinuous on c, d"
]

N_HYP = 3
NEG_Q_INDEX = 3