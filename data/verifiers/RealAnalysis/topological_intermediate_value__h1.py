import sympy
from sympy.abc import x

# Top-level setup
# The witness should be a tuple (X, f) where X is a sympy Set (or list/tuple/set of reals)
# and f is a sympy expression in x, a string, or a callable.

def conditions(witness) -> list[bool]:
    try:
        X, f = witness
    except Exception:
        return [False, False]
    
    try:
        if isinstance(X, (list, tuple, set)):
            X = sympy.FiniteSet(*X)
    except Exception:
        pass

    try:
        if isinstance(f, str):
            f_expr = sympy.sympify(f)
        elif callable(f):
            f_expr = f(x)
        else:
            f_expr = f
    except Exception:
        f_expr = f

    # H_1: f is continuous on X
    h1 = False
    try:
        if hasattr(sympy, 'continuous_domain'):
            try:
                cd = sympy.continuous_domain(f_expr, x, X)
                h1 = (cd == X)
            except Exception:
                # Fallback if continuous_domain raises an error
                if f_expr == x or f_expr.is_polynomial(x):
                    h1 = True
        else:
            # Fallback if continuous_domain is not available
            if f_expr == x or f_expr.is_polynomial(x):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: f(X) is not connected
    neg_q = False
    try:
        image = sympy.imageset(x, f_expr, X)
        
        def is_connected(S):
            if S == sympy.S.EmptySet:
                return True
            if isinstance(S, sympy.Interval):
                return True
            if isinstance(S, sympy.FiniteSet) and len(S) <= 1:
                return True
            if S == sympy.S.Reals:
                return True
            return False
        
        neg_q = not is_connected(image)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a continuous function on X",
    "¬Q: f(X) is not a connected subset of R (not an interval)"
]

N_HYP = 1
NEG_Q_INDEX = 1