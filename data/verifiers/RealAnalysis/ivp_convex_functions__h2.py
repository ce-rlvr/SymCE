import sympy
import math

x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If f is a real-valued function defined on an open interval (a, b), 
    then f has the intermediate value property on (a, b)."
    
    The witness should be a tuple (f_expr, a, b) where f_expr is a sympy expression 
    (or a Python callable) representing the function f, and a, b are the endpoints of the interval.
    """
    try:
        f_expr, a, b = witness
    except Exception:
        return [False, False]
    
    try:
        a_val = float(a)
        b_val = float(b)
    except Exception:
        return [False, False]
        
    if a_val >= b_val:
        return [False, False]
        
    # Determine a finite subinterval for sampling
    test_a = a_val
    test_b = b_val
    if math.isinf(a_val) and math.isinf(b_val):
        test_a, test_b = -10.0, 10.0
    elif math.isinf(a_val):
        test_a, test_b = b_val - 10.0, b_val
    elif math.isinf(b_val):
        test_a, test_b = a_val, a_val + 10.0

    # H_1: f is a real-valued function defined on (a, b)
    h1 = False
    try:
        all_real = True
        
        # Check for known singularities in the interval if it's a sympy expression
        if hasattr(f_expr, 'subs'):
            try:
                sings = sympy.singularities(f_expr, x)
                if isinstance(sings, sympy.Set):
                    inter = sympy.Intersection(sings, sympy.Interval.open(sympy.sympify(a), sympy.sympify(b)))
                    if inter.is_empty == False:
                        all_real = False
            except Exception:
                pass

        # Sample points to ensure it evaluates to real numbers
        if all_real:
            pts = [test_a + (test_b - test_a) * i / 100.0 for i in range(1, 100)]
            pts += [test_a + (test_b - test_a) * (i + 0.5) / 100.0 for i in range(1, 99)]
            for p in pts:
                if hasattr(f_expr, 'subs'):
                    val = f_expr.subs(x, p)
                    if not val.is_real or val.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
                        all_real = False
                        break
                else:
                    val = f_expr(p)
                    if not isinstance(val, (int, float)) or math.isnan(val) or math.isinf(val):
                        all_real = False
                        break
        h1 = all_real
    except Exception:
        h1 = False

    # ¬Q: f fails the intermediate value property on (a, b)
    neg_q = False
    try:
        if h1:
            # Sample points to find a jump discontinuity or gap in the image
            pts = [test_a + (test_b - test_a) * i / 100.0 for i in range(1, 100)]
            vals = []
            for p in pts:
                if hasattr(f_expr, 'subs'):
                    v = f_expr.subs(x, p)
                    vals.append((p, float(v)))
                else:
                    v = f_expr(p)
                    vals.append((p, float(v)))
            
            found_counterexample = False
            for i in range(len(vals) - 1):
                x1, y1 = vals[i]
                x2, y2 = vals[i+1]
                
                # If there is a significant gap between adjacent evaluated points
                if abs(y1 - y2) > 1e-3:
                    # Check a few intermediate values
                    for frac in [0.5, 0.25, 0.75]:
                        y_mid = y1 + (y2 - y1) * frac
                        
                        if hasattr(f_expr, 'subs'):
                            domain = sympy.Interval(x1, x2)
                            try:
                                sol = sympy.solveset(sympy.Eq(f_expr, y_mid), x, domain=domain)
                                is_empty = sol.is_empty
                            except Exception:
                                is_empty = None
                                
                            if is_empty == True:
                                found_counterexample = True
                                break
                            elif is_empty is None:
                                # Fallback to dense grid search if solveset cannot determine
                                try:
                                    f_lam = sympy.lambdify(x, f_expr, modules=['math'])
                                    dense_pts = [x1 + (x2 - x1) * m / 1000.0 for m in range(1001)]
                                    min_dist = min(abs(float(f_lam(p)) - y_mid) for p in dense_pts)
                                    if min_dist > 1e-3:
                                        found_counterexample = True
                                        break
                                except Exception:
                                    pass
                        else:
                            # Dense grid search for Python callables
                            dense_pts = [x1 + (x2 - x1) * m / 1000.0 for m in range(1001)]
                            min_dist = min(abs(float(f_expr(p)) - y_mid) for p in dense_pts)
                            if min_dist > 1e-3:
                                found_counterexample = True
                                break
                    if found_counterexample:
                        break
            neg_q = found_counterexample
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on an open interval (a, b)",
    "¬Q: f does not have the intermediate value property on (a, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1