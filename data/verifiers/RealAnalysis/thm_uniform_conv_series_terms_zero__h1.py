import sympy as sp
import math

# Top-level setup for potential witness expressions
R = sp.S.Reals
N_set = sp.S.Naturals
x, n = sp.symbols('x n')

def get_test_points(E):
    points = []
    try:
        if E.is_Interval:
            a = float(E.start) if E.start != -sp.oo else -100.0
            b = float(E.end) if E.end != sp.oo else 100.0
            if E.start == -sp.oo and E.end == sp.oo:
                a, b = -50.0, 50.0
            elif E.start == -sp.oo:
                a = b - 100.0
            elif E.end == sp.oo:
                b = a + 100.0
            
            num_points = 100
            if num_points > 1:
                step = (b - a) / (num_points - 1)
            else:
                step = 0
            points = [a + i * step for i in range(num_points)]
            
            # Add points close to boundaries to catch issues on open intervals
            if E.start != -sp.oo:
                points.extend([a + 1e-5, a + 1e-4, a + 1e-3])
            if E.end != sp.oo:
                points.extend([b - 1e-5, b - 1e-4, b - 1e-3])
                
        elif E.is_FiniteSet:
            points = [float(p) for p in E]
        else:
            points = [0.0, 1.0, -1.0, 2.0, -2.0, 5.0, -5.0, 10.0, -10.0]
    except Exception:
        points = [0.0, 1.0, -1.0, 2.0, -2.0]
    return points

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_expr = witness.get('f', witness.get('f_expr'))
            x_sym = witness.get('x', sp.Symbol('x'))
            n_sym = witness.get('n', sp.Symbol('n'))
            E = witness.get('E', sp.S.Reals)
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                f_expr, x_sym, n_sym, E = witness
            elif len(witness) == 2:
                f_expr, E = witness
                x_sym = sp.Symbol('x')
                n_sym = sp.Symbol('n')
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    points = get_test_points(E)
    
    try:
        f_func = sp.lambdify((n_sym, x_sym), f_expr, modules=['math'])
        if points:
            _ = float(f_func(1, points[0]))
    except Exception:
        f_func = lambda n_val, x_val: float(f_expr.subs({n_sym: n_val, x_sym: x_val}))
        
    # Check H1: sum f_n(x) converges uniformly on E
    # We check if the sequence of partial sums is uniformly Cauchy
    h1_ok = False
    try:
        errors = []
        for N in [50, 100, 200, 400]:
            max_err = 0.0
            valid_points = 0
            for x_val in points:
                try:
                    s = sum(float(f_func(k, x_val)) for k in range(N, 2*N))
                    if math.isnan(s):
                        continue
                    if math.isinf(s):
                        max_err = float('inf')
                        valid_points += 1
                        break
                    if abs(s) > max_err:
                        max_err = abs(s)
                    valid_points += 1
                except Exception:
                    continue
            if valid_points == 0 and len(points) > 0:
                max_err = float('inf')
            errors.append(max_err)
            
        if errors[-1] < 0.05:
            h1_ok = True
        elif errors[0] > 0 and errors[-1] < errors[0] * 0.4 and errors[-1] < 0.2:
            h1_ok = True
    except Exception:
        h1_ok = False

    # Check neg_Q: f_n(x) does NOT converge uniformly to 0 on E
    # We check if the supremum of |f_n(x)| fails to approach 0
    neg_q_ok = False
    try:
        max_vals = []
        for n_val in [10, 50, 100, 200, 500]:
            max_val = 0.0
            valid_points = 0
            for x_val in points:
                try:
                    val = float(abs(f_func(n_val, x_val)))
                    if math.isnan(val):
                        continue
                    if math.isinf(val):
                        max_val = float('inf')
                        valid_points += 1
                        break
                    if val > max_val:
                        max_val = val
                    valid_points += 1
                except Exception:
                    continue
            if valid_points == 0 and len(points) > 0:
                max_val = float('inf')
            max_vals.append(max_val)
            
        if max_vals[-1] > 0.05:
            neg_q_ok = True
        elif len(max_vals) > 1 and max_vals[-1] > 1e-3 and max_vals[-1] >= max_vals[-2]:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The infinite series sum_{n=1}^infty f_n(x) converges uniformly on E",
    "¬Q: The sequence of functions (f_n) does NOT converge uniformly to the zero function on E"
]

N_HYP = 1
NEG_Q_INDEX = 1