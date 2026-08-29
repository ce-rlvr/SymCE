import sympy
from sympy.ntheory import jacobi_symbol

CONDITION_LABELS = [
    "¬Q: sum_{a=1}^{p-1} (a/p) != 0"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        p = int(witness)
    except Exception:
        return [False]

    try:
        # The conclusion is sum_{a=1}^{p-1} (a/p) = 0.
        # We evaluate this using the Jacobi symbol, which generalizes the Legendre symbol.
        # If p is not an odd positive integer, jacobi_symbol raises an exception,
        # meaning the expression is undefined and the conclusion fails (neg_q = True).
        s = sum(jacobi_symbol(a, p) for a in range(1, p))
        neg_q = bool(s != 0)
    except Exception:
        neg_q = True

    return [neg_q]