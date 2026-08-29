import sympy
from sympy import Symbol, Interval, limit, S
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness function is uniformly continuous on (0, 1].
    A continuous function on a bounded interval (0, 1] is uniformly continuous
    if and only if its right-hand limit at 0 exists and is finite.
    """
    try:
        if callable(witness):
            expr = witness(x)
        else:
            expr = witness
            
        # Check if f is continuous on (0, 1]
        dom = continuous_domain(expr, x, Interval.Lopen(0, 1))
        if dom != Interval.Lopen(0, 1):
            neg_q = False
        else:
            # Check if the limit at 0+ exists and is finite
            L = limit(expr, x, 0, dir='+')
            
            if hasattr(L, 'has') and L.has(S.Infinity, S.NegativeInfinity, S.ComplexInfinity, S.NaN):
                neg_q = False
            elif type(L).__name__ == 'AccumBounds' or (hasattr(L, 'atoms') and any(type(arg).__name__ == 'AccumBounds' for arg in L.atoms())):
                neg_q = False
            elif type(L).__name__ == 'Limit' or (hasattr(L, 'has') and L.has(sympy.Limit)):
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["~Q: f is uniformly continuous on the given interval"]

N_HYP = 0
NEG_Q_INDEX = 0