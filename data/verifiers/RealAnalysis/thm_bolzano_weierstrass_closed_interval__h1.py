import sympy
from sympy import oo, Abs, limit
from sympy.abc import n
import math

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (x_n, a, b) where:
      - x_n is a sympy expression in terms of n (or a callable returning such an expression)
      - a and b are the endpoints of the interval (can be -oo, oo, or finite numbers)
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False]
        x_n, a, b = witness
    except Exception:
        return [False, False]
    
    if callable(x_n):
        try:
            expr = x_n(n)
        except Exception:
            expr = x_n
    else:
        expr = x_n

    # H_1: x_n in the interval for all n in N
    h1_ok = True
    try:
        if a == -oo:
            a_f = -float('inf')
        elif a == oo:
            a_f = float('inf')
        else:
            a_f = float(a)
            
        if b == -oo:
            b_f = -float('inf')
        elif b == oo:
            b_f = float('inf')
        else:
            b_f = float(b)
            
        for i in range(1, 101):
            val = expr.subs(n, i).evalf()
            if abs(sympy.im(val)) > 1e-9:
                h1_ok = False
                break
            val_f = float(sympy.re(val))
            if not (a_f <= val_f <= b_f):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: no subsequence converges to a real number L in the interval
    # This happens if and only if |x_n| -> oo as n -> oo.
    neg_q_ok = False
    try:
        L = limit(Abs(expr), n, oo)
        if L == oo:
            neg_q_ok = True
    except Exception:
        pass

    # Fallback for neg_Q if limit fails or returns unevaluated
    if not neg_q_ok:
        try:
            block1 = min(float(Abs(expr.subs(n, i)).evalf()) for i in range(100, 200))
            block2 = min(float(Abs(expr.subs(n, i)).evalf()) for i in range(1000, 1100))
            # If the sequence has no convergent subsequence, it eventually leaves every bounded interval
            if block2 > block1 + 100:
                neg_q_ok = True
        except Exception:
            pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x_n is a sequence of real numbers such that x_n is in the interval for all n",
    "not Q: There does not exist a subsequence converging to a real number L in the interval"
]

N_HYP = 1
NEG_Q_INDEX = 1