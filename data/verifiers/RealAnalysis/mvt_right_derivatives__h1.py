import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference
x = sympy.Symbol('x', real=True)

def eval_f(f_expr, val):
    try:
        if callable(f_expr):
            res = f_expr(val)
        else:
            res = f_expr.subs(x, val)
        return float(res)
    except Exception:
        return None

def right_derivative(f_expr, p):
    try:
        fp = eval_f(f_expr, p)
        if fp is None or math.isnan(fp): 
            return None
        
        h_vals = [1e-5, 1e-6, 1e-7, 1e-8]
        d = []
        for h in h_vals:
            val = eval_f(f_expr, p + h)
            if val is None or math.isnan(val):
                return None
            d.append((val - fp) / h)
            
        d1, d2, d3, d4 = d
        
        # Check for divergence
        if abs(d4) > 1e4 and abs(d4) > 5 * abs(d3):
            return None
            
        # Check for convergence with generous tolerance for floating point errors
        if abs(d4 - d3) < 1e-2 + 1e-2 * abs(d4) and abs(d3 - d2) < 1e-2 + 1e-2 * abs(d3):
            return d4
            
        return None
    except Exception:
        return None

def get_test_points(expr, a, b):
    points = set()
    # If it's a sympy expression, try to extract boundary points from conditions
    if not callable(expr):
        try:
            for rel in expr.atoms(sympy.Relational):
                try:
                    diff = rel.lhs - rel.rhs
                    sols = sympy.solve(diff, x)
                    for s in sols:
                        if s.is_real and a < float(s) < b:
                            points.add(float(s))
                except Exception:
                    pass
        except Exception:
            pass
            
    # Add a dense set of linearly spaced points
    step = (b - a) / 501.0
    for i in range(1, 501):
        points.add(a + i * step)
        
    return sorted(list(points))

def conditions(witness):
    try:
        f_expr, a, b = witness
        a_f = float(a)
        b_f = float(b)
    except Exception:
        return [False, False]
        
    if a_f >= b_f:
        return [False, False]
        
    test_points = get_test_points(f_expr, a_f, b_f)
    
    h1_ok = True
    derivs = []
    
    for p in test_points:
        d = right_derivative(f_expr, p)
        if d is None:
            # Fallback to exact sympy limit for points extremely close to a jump
            try:
                if not callable(f_expr):
                    h_sym = sympy.Symbol('h', positive=True)
                    diff_expr = (f_expr.subs(x, p + h_sym) - f_expr.subs(x, p)) / h_sym
                    lim = sympy.limit(diff_expr, h_sym, 0, dir='+')
                    if lim.is_real:
                        d = float(lim)
                    else:
                        h1_ok = False
                        break
                else:
                    h1_ok = False
                    break
            except Exception:
                h1_ok = False
                break
        derivs.append(d)
        
    neg_q_ok = False
    if h1_ok and derivs:
        try:
            fa = eval_f(f_expr, a_f)
            fb = eval_f(f_expr, b_f)
            if fa is not None and fb is not None:
                Q = (fb - fa) / (b_f - a_f)
                # The negation of the conclusion means it is impossible to find c1, c2 
                # such that f'_+(c1) <= Q <= f'_+(c2).
                # This happens if the right derivative is strictly less than Q everywhere,
                # or strictly greater than Q everywhere.
                all_less = all(d < Q - 1e-7 for d in derivs)
                all_greater = all(d > Q + 1e-7 for d in derivs)
                if all_less or all_greater:
                    neg_q_ok = True
        except Exception:
            pass
            
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The right derivative f'_+(x) exists for every x in (a, b)",
    "¬Q: For all c1, c2 in (a, b), it is not the case that f'_+(c1) <= (f(b)-f(a))/(b-a) <= f'_+(c2)"
]

N_HYP = 1
NEG_Q_INDEX = 1