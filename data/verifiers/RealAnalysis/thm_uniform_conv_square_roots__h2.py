import sympy as sp
import math

# Top-level setup
x, n = sp.symbols('x n')

def check_h1(f_n_expr, domain):
    lower, upper = domain
    lower = float(lower)
    
    grid = []
    if upper == sp.oo or upper == float('inf'):
        grid.append(lower)
        for i in range(1, 20):
            t = i / 20.0
            grid.append(lower + t / (1 - t))
    else:
        upper_f = float(upper)
        grid = [lower + (upper_f - lower) * i / 20.0 for i in range(21)]
        
    for n_val in [1, 2, 5, 10]:
        for x_val in grid:
            try:
                val_c = complex(f_n_expr.subs({'n': n_val, 'x': x_val}))
                if abs(val_c.imag) > 1e-7:
                    return False
                if val_c.real < -1e-5:
                    return False
            except Exception:
                pass
    return True

def check_pointwise_convergence(f_n_expr, f_expr, domain):
    lower, upper = domain
    lower = float(lower)
    
    grid = []
    if upper == sp.oo or upper == float('inf'):
        for i in range(1, 50):
            t = i / 50.0
            grid.append(lower + t / (1 - t))
    else:
        upper_f = float(upper)
        # Avoid exact boundaries to prevent false negatives on open intervals
        grid = [lower + (upper_f - lower) * i / 50.0 for i in range(1, 50)]
        
    for x_val in grid:
        try:
            val_f = complex(f_expr.subs({'x': x_val})).real
            val_fn_10k = complex(f_n_expr.subs({'n': 10000, 'x': x_val})).real
            if abs(val_fn_10k - val_f) > 0.05:
                val_fn_100k = complex(f_n_expr.subs({'n': 100000, 'x': x_val})).real
                if abs(val_fn_100k - val_f) > 0.05 and abs(val_fn_100k - val_f) >= 0.95 * abs(val_fn_10k - val_f):
                    return False
        except Exception:
            pass
    return True

def check_uniform_convergence(f_n_expr, f_expr, domain):
    lower, upper = domain
    lower = float(lower)
    
    def get_max_diff(n_val):
        grid = []
        if upper == sp.oo or upper == float('inf'):
            grid.append(lower)
            for i in range(1, 100):
                t = i / 100.0
                grid.append(lower + t / (1 - t))
            grid.extend([
                lower + 0.1/n_val, lower + 0.5/n_val, lower + 1.0/n_val, lower + 2.0/n_val,
                lower + 1/math.sqrt(n_val)
            ])
            valid_grid = [pt for pt in grid if pt >= lower]
        else:
            upper_f = float(upper)
            grid = [lower + (upper_f - lower) * i / 100.0 for i in range(101)]
            grid.extend([
                lower + 0.1/n_val, lower + 0.5/n_val, lower + 1.0/n_val, lower + 2.0/n_val,
                upper_f - 0.1/n_val, upper_f - 0.5/n_val, upper_f - 1.0/n_val, upper_f - 2.0/n_val,
                lower + (upper_f - lower)/math.sqrt(n_val),
                upper_f - (upper_f - lower)/math.sqrt(n_val)
            ])
            valid_grid = [pt for pt in grid if lower <= pt <= upper_f]
            
        valid_grid = sorted(list(set(valid_grid)))
        
        m_diff = 0.0
        for x_val in valid_grid:
            try:
                fn_val = complex(f_n_expr.subs({'n': n_val, 'x': x_val})).real
                f_val = complex(f_expr.subs({'x': x_val})).real
                if fn_val < 0: fn_val = 0.0
                if f_val < 0: f_val = 0.0
                diff = abs(math.sqrt(fn_val) - math.sqrt(f_val))
                if diff > m_diff:
                    m_diff = diff
            except Exception:
                pass
        return m_diff

    m_1000 = get_max_diff(1000)
    m_10000 = get_max_diff(10000)
    
    if m_10000 < 0.05:
        return True
        
    if m_10000 < 0.95 * m_1000:
        return True
        
    return False

def conditions(witness):
    """
    witness should be a dictionary:
    {
        'f_n': sympy expression in x and n,
        'f': sympy expression in x (the pointwise limit),
        'domain': tuple (lower_bound, upper_bound)
    }
    or a tuple (f_n, f, domain).
    """
    try:
        if isinstance(witness, dict):
            f_n_expr = witness.get('f_n')
            f_expr = witness.get('f')
            domain = witness.get('domain')
        else:
            f_n_expr, f_expr, domain = witness
            
        if isinstance(f_n_expr, str):
            f_n_expr = sp.sympify(f_n_expr)
        if isinstance(f_expr, str):
            f_expr = sp.sympify(f_expr)
            
        h1_ok = check_h1(f_n_expr, domain)
        
        pointwise_ok = check_pointwise_convergence(f_n_expr, f_expr, domain)
        
        if not pointwise_ok:
            neg_q_ok = False
        else:
            converges_uniformly = check_uniform_convergence(f_n_expr, f_expr, domain)
            neg_q_ok = not converges_uniformly
            
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of non-negative real-valued functions on E",
    "¬Q: The sequence (sqrt(f_n)) does not converge uniformly to sqrt(f) on E"
]

N_HYP = 1
NEG_Q_INDEX = 1