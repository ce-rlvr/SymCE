import math
import sympy
from sympy import Symbol

# Top-level setup for witness expressions
x = Symbol('x', real=True)
n = Symbol('n', integer=True)
k = Symbol('k', integer=True)
y = Symbol('y', real=True)

def conditions(witness) -> list[bool]:
    # Extract witness
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, f_obj = witness
    except Exception:
        return [False, False, False]

    # Check H1: [a,b] is a closed bounded interval in R
    try:
        a_val = float(a)
        b_val = float(b)
        h1 = a_val < b_val
    except Exception:
        h1 = False
        a_val, b_val = 0.0, 1.0

    # Extract the family of functions f_n(x)
    f = None
    if callable(f_obj):
        try:
            _ = float(f_obj(1, a_val))
            f = f_obj
        except Exception:
            try:
                _ = float(f_obj(1)(a_val))
                f = lambda n, x: f_obj(n)(x)
            except Exception:
                try:
                    _ = float(f_obj(a_val))
                    f = lambda n, x: f_obj(x)
                except Exception:
                    pass
    
    if f is None:
        try:
            if isinstance(f_obj, sympy.Expr):
                syms = sorted(list(f_obj.free_symbols), key=lambda s: s.name)
                if len(syms) == 2:
                    if syms[0].name == 'n':
                        n_var, x_var = syms[0], syms[1]
                    elif syms[1].name == 'n':
                        n_var, x_var = syms[1], syms[0]
                    else:
                        n_var, x_var = syms[0], syms[1]
                    f_lam = sympy.lambdify((n_var, x_var), f_obj, modules=['math', 'sympy'])
                    f = lambda n, x: float(f_lam(n, x))
                elif len(syms) == 1:
                    x_var = syms[0]
                    f_lam = sympy.lambdify((x_var,), f_obj, modules=['math', 'sympy'])
                    f = lambda n, x: float(f_lam(x))
                elif len(syms) == 0:
                    f = lambda n, x: float(f_obj)
        except Exception:
            pass

    # H2: M is the family of functions defined by g(x) = max_{a <= t <= x} f(t)
    h2 = (f is not None)

    # Check neg_Q: The family M is NOT equicontinuous on [a,b]
    neg_q = False
    if h1 and h2:
        try:
            N_grid = 10000
            xs = [a_val + i * (b_val - a_val) / N_grid for i in range(N_grid + 1)]
            
            n_values = [1, 2, 3, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000]
            
            W1 = 1000 # delta1 = (b-a)/10
            W3 = 1    # delta3 = (b-a)/10000
            
            Omega1 = 0.0
            Omega3 = 0.0
            omega3_n = []
            valid_n = []
            
            for nv in n_values:
                g = []
                current_max = -float('inf')
                valid = True
                for xi in xs:
                    try:
                        val = float(f(nv, xi))
                        if math.isinf(val) or math.isnan(val):
                            valid = False
                            break
                    except Exception:
                        valid = False
                        break
                    if val > current_max:
                        current_max = val
                    g.append(current_max)
                
                if not valid:
                    omega3_n.append(0.0)
                    valid_n.append(False)
                    continue
                    
                max_diff1 = 0.0
                for i in range(W1, N_grid + 1):
                    diff = g[i] - g[i-W1]
                    if diff > max_diff1:
                        max_diff1 = diff
                if max_diff1 > Omega1:
                    Omega1 = max_diff1
                    
                max_diff3 = 0.0
                for i in range(W3, N_grid + 1):
                    diff = g[i] - g[i-W3]
                    if diff > max_diff3:
                        max_diff3 = diff
                if max_diff3 > Omega3:
                    Omega3 = max_diff3
                    
                omega3_n.append(max_diff3)
                valid_n.append(True)
            
            # Condition 1: Variation doesn't shrink with delta (e.g., sin(nx), x^n)
            if Omega3 > 0.01 and Omega3 > 0.1 * Omega1:
                valid_omegas = [omega3_n[i] for i in range(len(n_values)) if valid_n[i]]
                if len(valid_omegas) >= 2:
                    num_first = min(3, len(valid_omegas) - 1)
                    omega_first = max(valid_omegas[:num_first])
                    if Omega3 > 1.1 * omega_first:
                        neg_q = True
            
            # Condition 2: Variation grows unboundedly with n (e.g., n*x)
            if not neg_q:
                valid_indices = [i for i in range(len(n_values)) if valid_n[i]]
                if len(valid_indices) >= 2:
                    first_idx = valid_indices[0]
                    last_idx = valid_indices[-1]
                    omega_early = omega3_n[first_idx]
                    omega_late = omega3_n[last_idx]
                    
                    if omega_late > 0.01 and omega_late > 5 * omega_early:
                        neg_q = True
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: interval is closed and bounded",
    "H_2: M is the family of running maxima",
    "not Q: M is not equicontinuous"
]

N_HYP = 2
NEG_Q_INDEX = 2