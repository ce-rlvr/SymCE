import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Check if the witness function is NOT uniformly continuous on R.
    Returns [neg_Q_ok].
    """
    neg_q = False
    
    if callable(witness):
        f = witness
    else:
        try:
            f_expr = sp.sympify(witness)
        except Exception:
            return [False]
            
        free_symbols = f_expr.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            var = x
        else:
            return [False]
            
        # 1. Check domain: if not defined on all of R, it's not uniformly continuous on R
        try:
            from sympy.calculus.util import continuous_domain
            domain = continuous_domain(f_expr, var, sp.S.Reals)
            if domain != sp.S.Reals:
                return [True]
        except Exception:
            pass

        # 2. Check limits of derivative at infinity
        try:
            df = sp.diff(f_expr, var)
            lim_inf = sp.limit(df, var, sp.oo)
            if lim_inf == sp.oo or lim_inf == -sp.oo:
                return [True]
            lim_minf = sp.limit(df, var, -sp.oo)
            if lim_minf == sp.oo or lim_minf == -sp.oo:
                return [True]
        except Exception:
            pass

        # 3. Setup for numerical check
        try:
            f = sp.lambdify(var, f_expr, modules=['math', 'sympy'])
        except Exception:
            return [False]
            
    # Numerical check for uniform continuity
    x_samples = []
    
    # Large values
    for i in range(1, 8):
        base = 10**i
        for mult in [1.0, 1.5, 2.0, 3.141592653589793, 5.0, 7.5]:
            x_samples.extend([base * mult, -base * mult])
            
    # Small values
    for i in range(1, 8):
        base = 10**(-i)
        for mult in [1.0, 1.5, 2.0, 3.141592653589793, 5.0, 7.5]:
            x_samples.extend([base * mult, -base * mult])
            
    # Dense grids
    for i in range(1, 1000):
        x_samples.append(i * 0.0001)
        x_samples.append(-i * 0.0001)
        x_samples.append(i * 100.0)
        x_samples.append(-i * 100.0)
        
    x_samples.extend([0.0, 0.5, -0.5, 1.0, -1.0, 2.0, -2.0])
    
    deltas = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    
    # We look for an epsilon > 0 such that for all delta > 0, 
    # there exist x, y with |x - y| < delta and |f(x) - f(y)| >= epsilon.
    for epsilon in [0.1, 0.5, 1.0]:
        all_deltas_failed = True
        for delta in deltas:
            found_pair = False
            for xv in x_samples:
                for dy in [delta/2, delta/3, delta/5, delta/10, 
                           -delta/2, -delta/3, -delta/5, -delta/10]:
                    yv = xv + dy
                    try:
                        val_x = float(f(xv))
                        val_y = float(f(yv))
                        if math.isnan(val_x) or math.isnan(val_y) or math.isinf(val_x) or math.isinf(val_y):
                            continue
                        if abs(val_x - val_y) >= epsilon:
                            found_pair = True
                            break
                    except Exception:
                        pass
                if found_pair:
                    break
            if not found_pair:
                all_deltas_failed = False
                break
        if all_deltas_failed:
            return [True]
            
    return [False]

CONDITION_LABELS = ["¬Q: f is not uniformly continuous on R"]
N_HYP = 0
NEG_Q_INDEX = 0