import sympy as sp
from sympy.abc import x, n
import math

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def make_callable_2(func):
    if callable(func):
        return func
    if hasattr(func, 'free_symbols'):
        syms = list(func.free_symbols)
        syms_str = [str(s) for s in syms]
        if 'n' in syms_str and 'x' in syms_str:
            n_sym = syms[syms_str.index('n')]
            x_sym = syms[syms_str.index('x')]
            return sp.lambdify((n_sym, x_sym), func, 'math')
        elif len(syms) == 2:
            return sp.lambdify((syms[0], syms[1]), func, 'math')
        elif len(syms) == 1:
            s = syms[0]
            f_lam = sp.lambdify(s, func, 'math')
            if str(s) == 'n':
                return lambda n_val, x_val: f_lam(n_val)
            else:
                return lambda n_val, x_val: f_lam(x_val)
        else:
            return lambda n_val, x_val: float(func)
    return lambda n_val, x_val: float(func)

def make_callable_1(func):
    if callable(func):
        return func
    if hasattr(func, 'free_symbols'):
        syms = list(func.free_symbols)
        if len(syms) == 1:
            return sp.lambdify(syms[0], func, 'math')
        else:
            return lambda x_val: float(func)
    return lambda x_val: float(func)

def get_domain_points(domain):
    try:
        if isinstance(domain, tuple) and len(domain) == 2:
            a, b = float(domain[0]), float(domain[1])
            if a > b:
                a, b = b, a
            return [a + (b - a) * i / 100.0 for i in range(101)]
        elif isinstance(domain, (list, set)):
            return [float(val) for val in domain]
        elif hasattr(domain, 'is_Interval') and domain.is_Interval:
            a = float(domain.start)
            b = float(domain.end)
            if a == -float('inf'): a = -1000
            if b == float('inf'): b = 1000
            return [a + (b - a) * i / 100.0 for i in range(101)]
        elif hasattr(domain, 'is_FiniteSet') and domain.is_FiniteSet:
            return [float(arg) for arg in domain.args]
    except Exception:
        pass
    return []

def is_subset(Y, X):
    if Y is None or X is None:
        return False
        
    try:
        if isinstance(Y, tuple) and len(Y) == 2:
            if float(Y[0]) > float(Y[1]):
                return False
        elif isinstance(Y, (list, set)):
            if len(Y) == 0:
                return False
        elif hasattr(Y, 'is_FiniteSet') and Y.is_FiniteSet:
            if len(Y) == 0:
                return False
                
        def point_in_X(p, X):
            try:
                p_val = float(p)
            except Exception:
                return False
                
            if isinstance(X, tuple) and len(X) == 2:
                a, b = float(X[0]), float(X[1])
                if a > b: a, b = b, a
                return a <= p_val <= b
            elif isinstance(X, (list, set)):
                for x_val in X:
                    try:
                        if abs(p_val - float(x_val)) < 1e-7:
                            return True
                    except Exception:
                        pass
                return False
            elif hasattr(X, 'is_Interval') and X.is_Interval:
                a, b = float(X.start), float(X.end)
                return a <= p_val <= b
            elif hasattr(X, 'is_FiniteSet') and X.is_FiniteSet:
                for x_val in X.args:
                    try:
                        if abs(p_val - float(x_val)) < 1e-7:
                            return True
                    except Exception:
                        pass
                return False
            return False

        if isinstance(Y, tuple) and len(Y) == 2:
            c, d = float(Y[0]), float(Y[1])
            if c > d: c, d = d, c
            if isinstance(X, tuple) and len(X) == 2:
                a, b = float(X[0]), float(X[1])
                if a > b: a, b = b, a
                return a <= c and d <= b
            elif hasattr(X, 'is_Interval') and X.is_Interval:
                a, b = float(X.start), float(X.end)
                return a <= c and d <= b
            else:
                return False
        elif isinstance(Y, (list, set)):
            return all(point_in_X(p, X) for p in Y)
        elif hasattr(Y, 'is_Interval') and Y.is_Interval:
            c, d = float(Y.start), float(Y.end)
            if isinstance(X, tuple) and len(X) == 2:
                a, b = float(X[0]), float(X[1])
                if a > b: a, b = b, a
                return a <= c and d <= b
            elif hasattr(X, 'is_Interval') and X.is_Interval:
                a, b = float(X.start), float(X.end)
                return a <= c and d <= b
            else:
                return False
        elif hasattr(Y, 'is_FiniteSet') and Y.is_FiniteSet:
            return all(point_in_X(p, X) for p in Y.args)
    except Exception:
        pass
    return False

def check_uniform_convergence(f_n, f, domain, domain_points):
    if not domain_points:
        return False
    ns = [10, 100, 1000, 10000, 100000]
    errors = []
    
    is_interval = False
    a, b = 0.0, 0.0
    try:
        if isinstance(domain, tuple) and len(domain) == 2:
            a, b = float(domain[0]), float(domain[1])
            if a > b: a, b = b, a
            is_interval = True
        elif hasattr(domain, 'is_Interval') and domain.is_Interval:
            a, b = float(domain.start), float(domain.end)
            if a == -float('inf'): a = -1000
            if b == float('inf'): b = 1000
            is_interval = True
    except Exception:
        pass
        
    for n_val in ns:
        max_err = 0.0
        evaluated_any = False
        
        pts = list(domain_points)
        if is_interval:
            try:
                pts.append(a + (b - a) / n_val)
                pts.append(b - (b - a) / n_val)
                if n_val > 0:
                    pts.append(a + (b - a) / math.sqrt(n_val))
                    pts.append(b - (b - a) / math.sqrt(n_val))
            except Exception:
                pass
            
        for x_val in pts:
            try:
                if is_interval:
                    x_val = max(a, min(b, x_val))
                val_n = f_n(n_val, x_val)
                val_f = f(x_val)
                err = abs(float(val_n) - float(val_f))
                if err > max_err:
                    max_err = err
                evaluated_any = True
            except Exception:
                pass
                
        if not evaluated_any:
            return False
            
        errors.append(max_err)
    
    if not errors:
        return False
        
    if errors[-1] < 1e-2 and errors[-1] <= errors[0] + 1e-7:
        return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_n = witness.get('f_n')
            f = witness.get('f')
            X = witness.get('X')
            Y = witness.get('Y')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            f_n, f, X, Y = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        f_n_call = make_callable_2(f_n)
        f_call = make_callable_1(f)
    except Exception:
        f_n_call = f_n
        f_call = f
        
    # H1: f_n converges uniformly to f on X
    try:
        X_points = get_domain_points(X)
        h1 = check_uniform_convergence(f_n_call, f_call, X, X_points)
    except Exception:
        h1 = False
        
    # H2: Y is a non-empty subset of X
    try:
        h2 = is_subset(Y, X)
    except Exception:
        h2 = False
        
    # neg_Q: f_n does NOT converge uniformly to f on Y
    try:
        Y_points = get_domain_points(Y)
        q = check_uniform_convergence(f_n_call, f_call, Y, Y_points)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The sequence (f_n) converges uniformly to a function f on X",
    "H_2: Let Y be a non-empty subset of X",
    "¬Q: The sequence (f_n) does not converge uniformly to f on the subset Y"
]

N_HYP = 2
NEG_Q_INDEX = 2