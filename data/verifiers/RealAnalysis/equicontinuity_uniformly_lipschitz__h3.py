import sympy as sp
import math
import itertools
import functools

# Top-level setup
x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)
t = sp.Symbol('t', real=True)
n = sp.Symbol('n', integer=True)
k = sp.Symbol('k', integer=True)

def get_test_functions(witness):
    funcs = []
    
    if isinstance(witness, dict):
        for key in ['funcs', 'family', 'functions', 'f', 'F']:
            if key in witness:
                return get_test_functions(witness[key])
        for v in witness.values():
            funcs.extend(get_test_functions(v))
        return funcs

    if hasattr(witness, '__dict__'):
        return get_test_functions(witness.__dict__)

    if isinstance(witness, (list, tuple, set)):
        for item in witness:
            if isinstance(item, sp.Expr):
                funcs.append(item)
            elif callable(item):
                try:
                    res = item(1)
                    if isinstance(res, sp.Expr):
                        funcs.append(res)
                except Exception:
                    pass
    elif isinstance(witness, sp.Expr):
        syms = list(witness.free_symbols)
        if len(syms) >= 2:
            n_sym = None
            for s in syms:
                if s.name in ['n', 'k', 'm']:
                    n_sym = s
                    break
            if n_sym is None:
                n_sym = syms[1]
            for n_val in [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]:
                funcs.append(witness.subs(n_sym, n_val))
        else:
            funcs.append(witness)
    elif callable(witness):
        for n_val in [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]:
            try:
                res = witness(n_val)
                if isinstance(res, sp.Expr):
                    funcs.append(res)
            except Exception:
                pass
    return funcs

def is_not_uniformly_equicontinuous(funcs):
    if not funcs:
        return False
    
    x_sym = None
    for f in funcs:
        if isinstance(f, sp.Expr):
            syms = list(f.free_symbols)
            if syms:
                for s in syms:
                    if s.name == 'x':
                        x_sym = s
                        break
                if x_sym is None:
                    x_sym = syms[0]
                break
    if x_sym is None:
        x_sym = sp.Symbol('x')
        
    deltas = [0.1, 0.01, 0.001, 0.0001]
    epsilons = [0.5, 0.2]
    
    x_vals = [0, 1, -1, 10, -10, 100, -100, 1000, -1000, 10000, -10000]
    for k_val in range(1, 6):
        x_vals.extend([
            1 - 10**(-k_val), -1 + 10**(-k_val),
            10**(-k_val), -10**(-k_val),
            10**k_val, -10**k_val
        ])
    for i in range(1, 100):
        x_vals.extend([i * 0.01, -i * 0.01, i * 0.001, -i * 0.001])
    x_vals.extend([3.14159265, 2.71828182])
    x_vals = list(set(x_vals))
    
    lambdified_funcs = []
    for f in funcs:
        if isinstance(f, sp.Expr):
            try:
                lf = sp.lambdify(x_sym, f, modules=['math', 'sympy'])
                lambdified_funcs.append(lf)
            except Exception:
                pass
                
    if not lambdified_funcs:
        return False

    for epsilon in epsilons:
        epsilon_fails = True
        for delta in deltas:
            found_large_diff = False
            for lf in lambdified_funcs:
                for xv in x_vals:
                    try:
                        val1 = float(lf(xv))
                        val2 = float(lf(xv + delta))
                        if abs(val1 - val2) >= epsilon:
                            found_large_diff = True
                            break
                    except Exception:
                        pass
                if found_large_diff:
                    break
            if not found_large_diff:
                epsilon_fails = False
                break
        if epsilon_fails:
            return True
            
    return False

def conditions(witness):
    try:
        funcs = get_test_functions(witness)
    except Exception:
        funcs = []
        
    try:
        h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = len(funcs) > 0
    except Exception:
        h2 = False
        
    try:
        neg_q = is_not_uniformly_equicontinuous(funcs)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: F is a family of functions from X to Y",
    "¬Q: F is not uniformly equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2