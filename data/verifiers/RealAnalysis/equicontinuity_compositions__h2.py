import sympy as sp
from sympy.calculus.util import continuous_domain, maximum

# Top-level setup for witness expressions
x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)
n = sp.Symbol('n', integer=True)
Reals = sp.Reals
Interval = sp.Interval

CONDITION_LABELS = [
    "H_1: X, Y, and Z are metric spaces",
    "H_2: g is a uniformly continuous function from Y to Z",
    "¬Q: The family of composite functions H = {g ∘ f | f ∈ F} is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Extract witness components
    g = witness.get('g')
    f = witness.get('f')
    X = witness.get('X')
    Y = witness.get('Y')
    Z = witness.get('Z', sp.Reals)
    x0 = witness.get('x0')
    epsilon = witness.get('epsilon')
    n_x_func = witness.get('n_x_func')
    
    # H_1: X, Y, and Z are metric spaces
    try:
        h1 = isinstance(X, sp.Set) and isinstance(Y, sp.Set) and isinstance(Z, sp.Set)
    except Exception:
        h1 = False
        
    # H_2: g is a uniformly continuous function from Y to Z
    try:
        h2 = False
        if isinstance(g, sp.Expr):
            is_unif_cont = False
            
            # Method 1: Compact domain + continuous function
            try:
                if Y.is_closed and Y.is_bounded:
                    if continuous_domain(g, y, Y) == Y:
                        is_unif_cont = True
            except Exception:
                pass
                
            # Method 2: Bounded derivative
            if not is_unif_cont:
                try:
                    g_prime = sp.diff(g, y)
                    max_val = maximum(sp.Abs(g_prime), y, Y)
                    if max_val.is_number and max_val < sp.oo:
                        is_unif_cont = True
                except Exception:
                    pass
                    
            if is_unif_cont:
                h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The family of composite functions H is not equicontinuous on X
    try:
        neg_q = False
        if isinstance(X, sp.Set) and isinstance(Y, sp.Set):
            in_X_x0 = X.contains(x0)
            if in_X_x0 == True or in_X_x0 == sp.S.true:
                if epsilon > 0:
                    # Test non-equicontinuity for a sequence of shrinking deltas
                    deltas = [1.0, 0.5, 0.1, 0.01, 0.001, 1e-4, 1e-5]
                    all_valid = True
                    for delta in deltas:
                        n_val, x_prime = n_x_func(delta)
                        
                        # Check if x_prime is in X
                        try:
                            in_X = X.contains(x_prime)
                            if in_X != True and in_X != sp.S.true:
                                all_valid = False
                                break
                        except Exception:
                            all_valid = False
                            break
                            
                        # Check if |x0 - x_prime| < delta
                        if abs(float(x0) - float(x_prime)) >= delta:
                            all_valid = False
                            break
                        
                        # Evaluate f_n(x0) and f_n(x_prime)
                        if isinstance(f, sp.Expr):
                            fn_x0 = f.subs({x: x0, n: n_val}).evalf()
                            fn_xprime = f.subs({x: x_prime, n: n_val}).evalf()
                        else:
                            fn_x0 = f(x0, n_val)
                            fn_xprime = f(x_prime, n_val)
                            
                        # Check if f maps into Y
                        try:
                            in_Y_x0 = Y.contains(fn_x0)
                            in_Y_xprime = Y.contains(fn_xprime)
                            if (in_Y_x0 != True and in_Y_x0 != sp.S.true) or \
                               (in_Y_xprime != True and in_Y_xprime != sp.S.true):
                                all_valid = False
                                break
                        except Exception:
                            all_valid = False
                            break
                            
                        # Evaluate g(f_n(x0)) and g(f_n(x_prime))
                        if isinstance(g, sp.Expr):
                            g_x0 = g.subs(y, fn_x0).evalf()
                            g_xprime = g.subs(y, fn_xprime).evalf()
                        else:
                            g_x0 = g(fn_x0)
                            g_xprime = g(fn_xprime)
                            
                        # Check if the difference is >= epsilon
                        if abs(float(g_x0) - float(g_xprime)) < float(epsilon):
                            all_valid = False
                            break
                            
                    if all_valid:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]