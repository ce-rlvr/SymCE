import sympy
import math
import itertools

x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f_expr, a, b) where:
      - f_expr is a sympy expression representing the function f(x)
      - a, b are real numbers defining the interval
    """
    try:
        f_expr, a, b = witness
    except Exception:
        return [False, False]
        
    # H_1: interval is a bounded closed interval in R
    try:
        a_val = float(a)
        b_val = float(b)
        h1 = (a_val <= b_val) and math.isfinite(a_val) and math.isfinite(b_val)
    except Exception:
        h1 = False
        
    # neg_Q: The family of functions is NOT uniformly equicontinuous on R
    try:
        if not hasattr(f_expr, 'free_symbols') or not f_expr.free_symbols:
            # Constant functions are uniformly equicontinuous
            neg_q = False
            return [h1, neg_q]
            
        free_syms = f_expr.free_symbols
        if x in free_syms:
            var = x
        else:
            var = list(free_syms)[0]
            
        # Symbolic check for linear functions (which are uniformly continuous)
        try:
            if sympy.diff(f_expr, var).is_constant():
                neg_q = False
                return [h1, neg_q]
        except Exception:
            pass

        modules = [
            {'Abs': abs, 
             'sign': lambda val: 1 if val > 0 else (-1 if val < 0 else 0),
             'Heaviside': lambda val: 1 if val >= 0 else 0},
            'math'
        ]
        f_lambda = sympy.lambdify(var, f_expr, modules=modules)
            
        epsilon = 0.5
        # We test a sequence of deltas. If for ALL deltas we can find a violation,
        # then the family is not uniformly equicontinuous.
        deltas = [1.0, 0.1, 0.01, 0.001, 0.0001, 1e-5, 1e-6]
        
        neg_q = True
        
        # Generate pseudo-random points using Weyl sequence + sine to avoid grid alignment issues
        x_vals = [0.0]
        seed = 1
        for scale in [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
            for _ in range(50):
                x_vals.append(scale * math.sin(seed * 12345.6789))
                seed += 1
        for scale in [1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8]:
            for _ in range(200):
                x_vals.append(scale * math.sin(seed * 12345.6789))
                seed += 1
                
        for delta in deltas:
            found = False
            cs = [a_val, b_val, (a_val + b_val) / 2.0]
            cs = list(set(cs))
            
            # Targeted points to catch jumps at 0
            targeted_x = [-delta * 0.1, -delta * 0.4, 0.0, delta * 0.1]
            
            for c in cs:
                if found: break
                if c == 0: continue
                
                for x_val in itertools.chain(x_vals, targeted_x):
                    y_val = x_val + delta * 0.5
                    try:
                        val_x = f_lambda(c * x_val)
                        val_y = f_lambda(c * y_val)
                        if isinstance(val_x, complex) or isinstance(val_y, complex):
                            continue
                        if math.isnan(val_x) or math.isnan(val_y):
                            continue
                        if abs(val_x - val_y) >= epsilon:
                            found = True
                            break
                    except Exception:
                        pass
            
            # If for some delta we cannot find any violation, it might be uniformly equicontinuous
            if not found:
                neg_q = False
                break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: interval is a bounded closed interval in R",
    "¬Q: The family of functions is not uniformly equicontinuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1