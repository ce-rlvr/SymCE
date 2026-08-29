import sympy as sp
import math
from sympy import Symbol, Interval, Piecewise, sin, cos, exp, log, oo, pi

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True)

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: The series sum_{n=1}^infty f_n converges uniformly on X",
    "¬Q: The family of partial sums is not equicontinuous on X"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) == 4:
            domain, f_expr, n_var, x_var = witness
            if hasattr(domain, 'inf') and hasattr(domain, 'sup'):
                a, b = float(domain.inf), float(domain.sup)
            else:
                a, b = float(domain[0]), float(domain[1])
            
            try:
                f_lam = sp.lambdify((n_var, x_var), f_expr, modules=['math'])
                # Test evaluation
                f_lam(1, a if math.isfinite(a) else 0.0)
                def f(n_val, x_val):
                    try:
                        return float(f_lam(n_val, x_val))
                    except Exception:
                        return float(f_expr.subs({n_var: n_val, x_var: x_val}))
            except Exception:
                def f(n_val, x_val):
                    return float(f_expr.subs({n_var: n_val, x_var: x_val}))
        elif len(witness) == 2:
            f_in, domain = witness
            if hasattr(domain, 'inf') and hasattr(domain, 'sup'):
                a, b = float(domain.inf), float(domain.sup)
            else:
                a, b = float(domain[0]), float(domain[1])
            def f(n_val, x_val):
                return float(f_in(n_val, x_val))
        else:
            return [False, False, False]
            
        if not (a < b):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: X is a metric space (any valid real interval is a metric space)
    h1 = True
    
    a_test = a if math.isfinite(a) else -100.0
    b_test = b if math.isfinite(b) else 100.0
    
    # Shift grid slightly to avoid boundary singularities
    eps = 1e-7
    a_safe = a_test + eps
    b_safe = b_test - eps
    if a_safe >= b_safe:
        a_safe, b_safe = a_test, b_test
    
    # H2: Uniform convergence of the series
    try:
        grid = [a_safe + i*(b_safe-a_safe)/500 for i in range(501)]
        
        max_tail = 0
        for x_val in grid:
            tail = sum(f(k, x_val) for k in range(100, 121))
            max_tail = max(max_tail, abs(tail))
            
        max_tail_early = 0
        for x_val in grid:
            tail = sum(f(k, x_val) for k in range(30, 51))
            max_tail_early = max(max_tail_early, abs(tail))
            
        # Check Cauchy criterion for uniform convergence
        h2 = bool(max_tail < 0.05 and max_tail <= max_tail_early + 1e-4)
    except Exception:
        h2 = False
        
    # neg_Q: The family of partial sums {S_N} is NOT equicontinuous
    try:
        neg_q = False
        # We check if there is a persistent jump in S_N for some N as grid resolution increases.
        # A continuous function's max jump between adjacent grid points decreases as delta -> 0.
        # A discontinuous function's max jump remains roughly constant.
        for N in range(1, 6):
            max_jumps = []
            for num_points in [1000, 3000, 9000, 27000]:
                delta = (b_safe - a_safe) / num_points
                grid_delta = [a_safe + i*delta for i in range(num_points + 1)]
                
                max_jump = 0
                prev_val = sum(f(k, grid_delta[0]) for k in range(1, N+1))
                for i in range(1, num_points + 1):
                    val = sum(f(k, grid_delta[i]) for k in range(1, N+1))
                    jump = abs(val - prev_val)
                    if jump > max_jump:
                        max_jump = jump
                    prev_val = val
                max_jumps.append(max_jump)
            
            # If the jump doesn't decrease significantly (ratio > 0.85) and is non-trivial (> 0.01),
            # the function is discontinuous, hence the family is not equicontinuous.
            if max_jumps[-1] > 0.01 and max_jumps[-1] > 0.85 * max_jumps[-2]:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]