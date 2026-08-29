import sympy
from sympy import Symbol, Expr, diff, limit, oo, Abs

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Any function between metric spaces is uniformly continuous."
    
    The witness should be a sympy expression in terms of x, representing a function f: R -> R.
    """
    # H_1: X and Y are metric spaces
    # We assume the domain and codomain are subsets of R, which are metric spaces.
    h1 = True
    
    # H_2: f: X \to Y is a function
    try:
        if callable(witness):
            f = witness(x)
        else:
            f = witness
        h2 = isinstance(f, Expr)
    except Exception:
        h2 = False
        f = None

    # neg_Q: f is NOT uniformly continuous on its domain
    neg_q = False
    if h2 and f is not None:
        try:
            df = diff(f, x)
        except Exception:
            df = sympy.S.Zero
            
        # Check 1: Unbounded derivative at infinity
        try:
            if limit(Abs(df), x, oo) == oo:
                neg_q = True
        except Exception:
            pass
            
        try:
            if not neg_q and limit(Abs(df), x, -oo) == oo:
                neg_q = True
        except Exception:
            pass
            
        # Check 2: f(x + 1/x) - f(x) doesn't go to 0 as x -> oo
        if not neg_q:
            try:
                diff_expr = Abs(f.subs(x, x + 1/x) - f)
                L = limit(diff_expr, x, oo)
                if L != 0 and not isinstance(L, sympy.Limit):
                    neg_q = True
            except Exception:
                pass
                
        # Check 3: Unbounded near common singularities (e.g., 1/x near 0)
        if not neg_q:
            try:
                for val in [0, sympy.pi/2, sympy.pi, 1, -1]:
                    if limit(Abs(f), x, val, dir='+') == oo or limit(Abs(f), x, val, dir='-') == oo:
                        neg_q = True
                        break
            except Exception:
                pass
                
        # Check 4: Max derivative grows with the interval (catches oscillatory unbounded derivatives like sin(x^2))
        if not neg_q:
            try:
                max_100 = max([abs(float(df.subs(x, val))) for val in range(1, 101)])
                max_1000 = max([abs(float(df.subs(x, val))) for val in range(1000, 1101)])
                if max_1000 > max_100 * 2 and max_1000 > 10:
                    neg_q = True
            except Exception:
                pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are metric spaces",
    "H_2: f: X \\to Y is a function",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2