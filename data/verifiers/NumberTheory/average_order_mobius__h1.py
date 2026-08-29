import sympy
from sympy import Symbol, Sum, limit, oo
import math

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', integer=True, positive=True)

def conditions(witness):
    try:
        expr = None
        # Check if witness is a callable function
        if callable(witness):
            try:
                expr = witness(n)
            except Exception:
                pass
        else:
            expr = witness
            # If it's an expression with a single free symbol, substitute it with 'n'
            if hasattr(expr, 'free_symbols') and len(expr.free_symbols) == 1:
                sym = list(expr.free_symbols)[0]
                expr = expr.subs(sym, n)
            else:
                expr = sympy.sympify(witness)
                
        # Attempt symbolic evaluation first
        if expr is not None:
            s = Sum(expr, (n, 1, x)).doit()
            avg = s / x
            L = limit(avg, x, oo)
            
            if L.is_number or L in [oo, -oo]:
                neg_q = bool(L != 0)
                return [neg_q]
                
        # Numerical fallback if symbolic evaluation fails or yields an unevaluated limit
        if callable(witness):
            func = witness
        else:
            func = sympy.lambdify(n, expr, 'math')
            
        # Evaluate the average for a reasonably large x
        total = sum(func(i) for i in range(1, 5001))
        avg_val = total / 5000.0
        
        # If the limit is 0, the average should be close to 0.
        # A counterexample will typically have an average significantly far from 0.
        neg_q = abs(avg_val) > 1e-2
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: lim_{x -> oo} (1/x) sum_{n=1}^x mu(n) != 0"
]

N_HYP = 0
NEG_Q_INDEX = 0