import sympy
from sympy import Symbol, limit, oo, S

# Top-level setup
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (expr, L) or a dict {'x_n': expr, 'L': L},
    where expr is the sequence expression in terms of n, and L is the proposed limit.
    """
    # H_1: (x_n) is a Cauchy sequence of real numbers
    try:
        if isinstance(witness, dict):
            expr = witness.get('x_n', witness.get('expr'))
            L = witness.get('L')
        else:
            expr, L = witness
            
        if callable(expr):
            expr = expr(n)
            
        expr = sympy.sympify(expr)
        
        lim = limit(expr, n, oo)
        
        # A sequence of reals is Cauchy iff it converges to a finite real number
        if lim.has(sympy.AccumBounds):
            h1_ok = False
        else:
            h1_ok = (lim in S.Reals) or bool(lim.is_real and lim.is_finite)
            
    except Exception:
        h1_ok = False

    # ¬Q: The entire sequence (x_n) does not converge to L
    try:
        if isinstance(witness, dict):
            expr = witness.get('x_n', witness.get('expr'))
            L = witness.get('L')
        else:
            expr, L = witness
            
        if callable(expr):
            expr = expr(n)
            
        expr = sympy.sympify(expr)
        L = sympy.sympify(L)
        
        lim = limit(expr, n, oo)
        
        if lim.has(sympy.AccumBounds):
            neg_q_ok = True
        else:
            diff = sympy.simplify(lim - L)
            neg_q_ok = bool(diff != 0)
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (x_n) is a Cauchy sequence of real numbers",
    "¬Q: The entire sequence (x_n) does not converge to L"
]

N_HYP = 1
NEG_Q_INDEX = 1