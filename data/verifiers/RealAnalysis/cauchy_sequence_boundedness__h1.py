import sympy
from sympy import Symbol, oo
from sympy.calculus.util import AccumBounds, maximum, minimum
from sympy import Interval

# Top-level setup for the witness expression
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If (x_n) is a Cauchy sequence, then (x_n) is bounded."
    """
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
        expr = sympy.sympify(expr)
    except Exception:
        return [False, False]

    # H_1: (x_n) is a Cauchy sequence
    # In R, a sequence is Cauchy iff it converges to a finite limit.
    h1_ok = False
    try:
        valid_terms = True
        # Check for singularities in the first 100 terms
        for i in range(1, 101):
            val = expr.subs(n, i)
            if not val.is_finite:
                valid_terms = False
                break
        
        if valid_terms:
            L = sympy.limit(expr, n, oo)
            if not isinstance(L, AccumBounds) and L.is_finite:
                h1_ok = True
    except Exception:
        h1_ok = False

    # Q: The sequence (x_n) is bounded
    q_ok = False
    try:
        valid_terms = True
        for i in range(1, 101):
            val = expr.subs(n, i)
            if not val.is_finite:
                valid_terms = False
                break
        
        if valid_terms:
            L = sympy.limit(expr, n, oo)
            if isinstance(L, AccumBounds):
                if L.max.is_finite and L.min.is_finite:
                    q_ok = True
            elif L.is_finite:
                q_ok = True
            elif L == oo or L == -oo:
                q_ok = False
            else:
                # Fallback for unevaluated limits
                max_val = maximum(expr, n, Interval(1, oo))
                min_val = minimum(expr, n, Interval(1, oo))
                if max_val.is_finite and min_val.is_finite:
                    q_ok = True
    except Exception:
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (x_n) is a Cauchy sequence",
    "¬Q: The sequence (x_n) is not bounded"
]

N_HYP = 1
NEG_Q_INDEX = 1