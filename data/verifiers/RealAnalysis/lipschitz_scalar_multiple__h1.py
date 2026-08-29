import math
import sympy
from sympy import symbols, Rational, Integer, Float, oo, nan

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def dist(a, b):
    if isinstance(a, (tuple, list, sympy.Tuple)) and isinstance(b, (tuple, list, sympy.Tuple)):
        return math.sqrt(sum((float(u) - float(v))**2 for u, v in zip(a, b)))
    else:
        return abs(a - b)

def evaluate(f, val):
    if callable(f):
        return f(val)
    elif isinstance(f, dict):
        return f[val]
    elif hasattr(f, 'free_symbols'):
        syms = list(f.free_symbols)
        if len(syms) == 1:
            return f.subs(syms[0], val)
        elif len(syms) == 0:
            return float(f)
        else:
            raise ValueError("Expression has more than one free symbol")
    else:
        raise ValueError("f must be callable, dict, or sympy expression")

def is_lipschitz(f, X, L):
    for a in X:
        for b in X:
            if a == b:
                continue
            d = dist(a, b)
            if d == 0:
                continue
            
            fa = evaluate(f, a)
            fb = evaluate(f, b)
            diff = abs(fa - fb)
            bound = L * d
            
            try:
                bound_float = float(bound)
            except Exception:
                return False
                
            if math.isnan(bound_float):
                return False
                
            try:
                diff_float = float(diff)
            except Exception:
                return False
                
            if not (diff_float <= bound_float):
                return False
    return True

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (f, X, L, c)
    where:
      - f is a callable, dict, or sympy expression representing the function
      - X is a list or iterable of points in the domain
      - L is the Lipschitz constant (can be math.inf)
      - c is the scalar multiplier
    """
    try:
        f, X, L, c = witness
    except Exception:
        return [False, False, False]
    
    # H_1: f is Lipschitz continuous with constant L
    try:
        h1 = is_lipschitz(f, X, L)
    except Exception:
        h1 = False
        
    # H_2: c is a real number
    try:
        if isinstance(c, complex):
            h2 = False
        else:
            c_float = float(c)
            h2 = not math.isnan(c_float) and not math.isinf(c_float)
    except Exception:
        h2 = False
        
    # ¬Q: cf is NOT Lipschitz continuous with constant |c|L
    try:
        def cf(val):
            return c * evaluate(f, val)
        
        abs_c = abs(c)
        c_L = abs_c * L
        
        q = is_lipschitz(cf, X, c_L)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous with constant L",
    "H_2: c is a real number",
    "¬Q: cf is NOT Lipschitz continuous with constant |c|L"
]

N_HYP = 2
NEG_Q_INDEX = 2