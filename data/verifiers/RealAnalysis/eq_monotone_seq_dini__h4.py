import math
import sympy
from sympy import symbols

# Top-level setup for witness expressions
n, x = symbols('n x')

def pseudo_random(num):
    """Generate pseudo-random numbers in [0, 1) deterministically."""
    return [(math.sin(i * 12.9898) * 43758.5453) % 1.0 for i in range(1, num + 1)]

def get_f_func(witness):
    """Extract the interval [a, b] and the sequence of functions f_n(x)."""
    a, b, f = witness
    if callable(f):
        return float(a), float(b), f, None
    else:
        n_sym, x_sym = symbols('n x')
        f_expr = sympy.sympify(f)
        # Use Python's max/min/abs for speed if the expression contains them
        modules = [{'Max': max, 'Min': min, 'Abs': abs}, 'math', 'sympy']
        f_lam = sympy.lambdify((n_sym, x_sym), f_expr, modules=modules)
        return float(a), float(b), f_lam, f_expr

def conditions(witness) -> list[bool]:
    try:
        a, b, f_func, f_expr = get_f_func(witness)
    except Exception:
        return [False, False, False, False]

    # H_1: X is a compact topological space
    # In R, this means a closed and bounded interval [a, b] with a <= b.
    try:
        h1 = (a <= b) and math.isfinite(a) and math.isfinite(b)
    except Exception:
        h1 = False

    # H_2: {f_n} is a sequence of continuous real-valued functions on X
    try:
        h2 = True
        for i in range(1, 6):
            if f_expr is not None:
                try:
                    from sympy.calculus.util import continuous_domain
                    from sympy import Interval, S
                    domain = continuous_domain(f_expr.subs(n, i), x, S.Reals)
                    if not Interval(a, b).is_subset(domain):
                        h2 = False
                        break
                except Exception:
                    pass # Fallback to heuristic check
            
            # Heuristic check for continuity and real-valuedness
            xs = [a + j*(b-a)/1000 for j in range(1001)]
            ys = []
            for x_val in xs:
                try:
                    val = float(f_func(i, x_val))
                    if math.isnan(val) or math.isinf(val):
                        h2 = False
                        break
                    ys.append(val)
                except Exception:
                    h2 = False
                    break
            if not h2:
                break
            
            # Check for large jumps as a sign of discontinuity
            for j in range(len(ys)-1):
                if abs(ys[j+1] - ys[j]) > 10000:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H_3: For all x \in X and n \in \mathbb{N}, f_{n+1}(x) \le f_n(x)
    try:
        h3 = True
        for i in range(1, 21):
            xs = [a + j*(b-a)/100 for j in range(101)]
            xs += [a + (b-a)*r for r in pseudo_random(100)]
            for x_val in xs:
                try:
                    y_n = float(f_func(i, x_val))
                    y_n1 = float(f_func(i+1, x_val))
                    # Allow a small floating point tolerance
                    if y_n1 > y_n + max(1e-7, 1e-7 * abs(y_n)):
                        h3 = False
                        break
                except Exception:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # ¬Q: The sequence {f_n} is NOT an equicontinuous family on X
    # We check if there exists an eps > 0 such that for all delta > 0, 
    # there is an n and x1, x2 with |x1 - x2| < delta and |f_n(x1) - f_n(x2)| > eps.
    try:
        neg_q = True
        eps = 0.05
        deltas = [0.1, 0.01, 0.001, 0.0001, 0.00001]
        ns = [1, 10, 100, 1000, 10000, 100000, 1000000]
        
        for delta in deltas:
            found_for_delta = False
            for i in ns:
                xs = [a + j*(b-a)/1000 for j in range(1001)]
                xs += [a + (b-a)*r for r in pseudo_random(1000)]
                xs += [a, max(a, b - delta * 0.9)]
                
                for x1 in xs:
                    x2 = min(b, x1 + delta * 0.9)
                    try:
                        y1 = float(f_func(i, x1))
                        y2 = float(f_func(i, x2))
                        if abs(y2 - y1) > eps:
                            found_for_delta = True
                            break
                    except OverflowError:
                        # If it overflows, the function is growing unboundedly, hence not equicontinuous
                        found_for_delta = True
                        break
                    except Exception:
                        pass
                if found_for_delta:
                    break
            if not found_for_delta:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact topological space",
    "H_2: {f_n} is a sequence of continuous real-valued functions on X",
    "H_3: For all x in X and n in N, f_{n+1}(x) <= f_n(x)",
    "¬Q: The sequence {f_n} is not an equicontinuous family on X"
]

N_HYP = 3
NEG_Q_INDEX = 3