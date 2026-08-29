import sympy as sp
from sympy.abc import x, h, t
import math

# Top-level setup for Real Analysis
# (No specific algebraic groups are needed for this domain)

def conditions(witness) -> list[bool]:
    """
    Given a witness function f, checks if it satisfies the hypotheses and fails the conclusion.
    """
    # Extract the function if the witness is a tuple
    if isinstance(witness, tuple):
        f = witness[0]
    else:
        f = witness

    # If the witness is a callable rather than a sympy expression, try to convert it
    if not isinstance(f, sp.Expr) and callable(f):
        try:
            f = f(x)
        except Exception:
            pass

    # H_1: f is uniformly continuous on R
    h1_ok = False
    try:
        if isinstance(f, sp.Expr):
            free_syms = f.free_symbols
            if x in free_syms:
                var = x
            elif len(free_syms) == 1:
                var = list(free_syms)[0]
            else:
                var = x

            # Heuristic check for uniform continuity:
            # We check if the function has bounded variations for a small delta over a wide range of points.
            delta = 0.001
            test_points = [0, 1, 10, 100, 1000, 10000, 100000, 10**6, 10**7, 10**8, 10**9]
            # Add a dense grid to catch highly oscillating functions
            for i in range(50):
                test_points.append(1000 + i * 0.1)
                
            f_num_h1 = sp.lambdify(var, f, 'math')
            
            h1_ok = True
            for val in test_points:
                for sign in [1, -1]:
                    v = sign * val
                    try:
                        # Try fast numerical evaluation first
                        try:
                            v1 = f_num_h1(v + delta)
                            v2 = f_num_h1(v)
                            c1 = complex(v1)
                            c2 = complex(v2)
                        except Exception:
                            # Fallback to symbolic substitution if math domain errors occur
                            v1 = f.subs(var, v + delta).evalf()
                            v2 = f.subs(var, v).evalf()
                            c1 = complex(v1)
                            c2 = complex(v2)
                            
                        if abs(c1.imag) > 1e-9 or abs(c2.imag) > 1e-9:
                            h1_ok = False
                            break
                        if abs(c1.real - c2.real) > 0.5:
                            h1_ok = False
                            break
                    except Exception:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: f_h is the Steklov average of f
    # This is definitional. If f is a valid expression, we consider this hypothesis satisfied.
    h2_ok = False
    try:
        if isinstance(f, sp.Expr):
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: f_h does NOT converge uniformly to f on R as h -> 0
    neg_q_ok = False
    try:
        if isinstance(f, sp.Expr):
            free_syms = f.free_symbols
            if x in free_syms:
                var = x
            elif len(free_syms) == 1:
                var = list(free_syms)[0]
            else:
                var = x

            f_num = sp.lambdify(var, f, 'math')
            
            h_val = 0.01
            test_points = [0, 1, 10, 100, 1000, 10000, 100000]
            # Add a dense grid to catch functions where the difference is large only at specific phases
            for i in range(50):
                test_points.append(10000 + i * 0.05)
                
            for v in test_points:
                for sign in [1, -1]:
                    val = sign * v
                    try:
                        f_val = f_num(val)
                        
                        # Numerically integrate f over [val - h_val, val + h_val] using the midpoint rule
                        steps = 1000
                        dt = 2 * h_val / steps
                        integral = 0.0
                        for i in range(steps):
                            t_val = val - h_val + (i + 0.5) * dt
                            integral += f_num(t_val) * dt
                        f_h_val = integral / (2 * h_val)
                        
                        # If the difference is significant for a small h, uniform convergence fails
                        if abs(f_h_val - f_val) > 0.1:
                            neg_q_ok = True
                            break
                    except Exception:
                        # Ignore points where evaluation overflows or is undefined
                        pass
                if neg_q_ok:
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on R",
    r"H_2: f_h(x) = (1/(2h)) \int_{x-h}^{x+h} f(t) dt is the Steklov average of f for h > 0",
    "¬Q: The family of functions f_h does not converge uniformly to f on R as h -> 0"
]

N_HYP = 2
NEG_Q_INDEX = 2