import sympy
from sympy import Symbol, Interval, solveset

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, a, b) where:
      - f is a sympy expression in terms of x (or a callable)
      - a and b are real numbers (the endpoints of the interval)
    """
    try:
        f, a, b = witness
        if isinstance(f, str):
            f = sympy.sympify(f)
        if isinstance(a, str):
            a = sympy.sympify(a)
        if isinstance(b, str):
            b = sympy.sympify(b)
    except Exception:
        return [False, False]
        
    # H_1: f(a) and f(b) have opposite signs (f(a)f(b) < 0)
    try:
        if callable(f):
            fa = f(a)
            fb = f(b)
        else:
            fa = f.subs(x, a)
            fb = f.subs(x, b)
        
        # Try evaluating to float to avoid symbolic inequality issues
        try:
            fa_val = float(fa)
            fb_val = float(fb)
            h1 = (fa_val * fb_val < 0)
        except TypeError:
            h1 = bool(fa * fb < 0)
    except Exception:
        h1 = False

    # neg_Q: There exists NO point c in the open interval (a, b) such that f(c) = 0
    try:
        lower = min(a, b)
        upper = max(a, b)
        
        if callable(f):
            # We cannot reliably prove a callable has no roots over an interval
            neg_q = False
        else:
            roots = solveset(f, x, domain=Interval.open(lower, upper))
            if roots.is_empty == True:
                neg_q = True
            elif roots.is_empty == False:
                neg_q = False
            else:
                # If sympy cannot determine if the set is empty, we must return False
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(a) and f(b) have opposite signs (f(a)f(b) < 0)",
    "¬Q: There exists no point c in the open interval (a, b) such that f(c) = 0"
]

N_HYP = 1
NEG_Q_INDEX = 1