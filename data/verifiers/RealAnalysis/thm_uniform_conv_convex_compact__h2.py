import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference
x, n = sp.symbols('x n', real=True)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of convex real-valued functions defined on an open interval (a, b)",
    "H_2: K is a compact subset of (a, b)",
    "¬Q: The sequence (f_n) does not converge uniformly to f on the compact subset K"
]

def check_H1(witness):
    f_n_expr = witness['f_n']
    a = witness['a']
    b = witness['b']
    
    a_num = -100.0 if a == -sp.oo else float(a)
    b_num = 100.0 if b == sp.oo else float(b)
    
    if a_num >= b_num:
        return False
        
    # Create a grid of points strictly inside (a, b)
    points = [a_num + (b_num - a_num) * i / 20.0 for i in range(1, 20)]
    
    f_n_func = sp.lambdify((x, n), f_n_expr, 'math')
    
    # Check convexity for a few values of n
    for i in [1, 2, 3, 10, 100]:
        for j in range(len(points)):
            for k in range(j + 1, len(points)):
                p1 = points[j]
                p2 = points[k]
                t = 0.5
                pt = t * p1 + (1 - t) * p2
                try:
                    val1 = f_n_func(p1, i)
                    val2 = f_n_func(p2, i)
                    valt = f_n_func(pt, i)
                    # Midpoint convexity check with a small tolerance for floating point errors
                    if valt > t * val1 + (1 - t) * val2 + 1e-5:
                        return False
                except Exception:
                    # If the function cannot be evaluated (e.g., not real-valued), it fails H1
                    return False
    return True

def check_H2(witness):
    a = witness['a']
    b = witness['b']
    K = witness['K']
    k_min, k_max = float(K[0]), float(K[1])
    
    if k_min > k_max:
        return False
        
    if a == -sp.oo:
        a_ok = True
    else:
        a_ok = float(a) < k_min
        
    if b == sp.oo:
        b_ok = True
    else:
        b_ok = k_max < float(b)
        
    return a_ok and b_ok

def check_neg_Q(witness):
    f_n_expr = witness['f_n']
    K = witness['K']
    k_min, k_max = float(K[0]), float(K[1])
    
    # Check pointwise convergence at a few points first
    points_few = [k_min + (k_max - k_min) * i / 10.0 for i in range(11)]
    
    if 'f' in witness:
        f_expr = witness['f']
        for p in points_few:
            try:
                diff = f_n_expr.subs(x, p) - f_expr.subs(x, p)
                lim = sp.limit(diff, n, sp.oo)
                if lim != 0:
                    return True
            except Exception:
                pass # Fallback to numerical uniform convergence check
                
        # Check uniform convergence over a dense grid
        points_many = [k_min + (k_max - k_min) * i / 100000.0 for i in range(100001)]
        f_n_func = sp.lambdify((x, n), f_n_expr, 'math')
        f_func = sp.lambdify(x, f_expr, 'math')
        
        try:
            md = max(abs(f_n_func(p, 100000) - f_func(p)) for p in points_many)
            if md > 0.1:
                return True
        except Exception:
            # Overflow or domain errors at large n imply non-uniform convergence
            return True
            
        return False
    else:
        # If f is not provided, check if the sequence is uniformly Cauchy
        points_many = [k_min + (k_max - k_min) * i / 100000.0 for i in range(100001)]
        f_n_func = sp.lambdify((x, n), f_n_expr, 'math')
        try:
            md = max(abs(f_n_func(p, 50000) - f_n_func(p, 100000)) for p in points_many)
            if md > 0.05:
                return True
        except Exception:
            return True
        return False

def conditions(witness):
    try:
        H1 = check_H1(witness)
    except Exception:
        H1 = False

    try:
        H2 = check_H2(witness)
    except Exception:
        H2 = False

    try:
        neg_Q = check_neg_Q(witness)
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]