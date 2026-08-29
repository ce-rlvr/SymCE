import sympy
from sympy.ntheory import factorint

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    r"¬Q: \lambda(mn) \neq \lambda(m)\lambda(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def liouville(x):
    """
    Computes the Liouville function \lambda(n) = (-1)^{\Omega(n)}.
    It is strictly defined only for positive integers.
    """
    if not (isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool)):
        raise ValueError("Liouville function is only defined for integers.")
    if x <= 0:
        raise ValueError("Liouville function is only defined for positive integers.")
    
    f = factorint(x)
    return (-1) ** sum(f.values())

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            m = witness['m']
            n = witness['n']
        elif hasattr(witness, 'm') and hasattr(witness, 'n'):
            m = witness.m
            n = witness.n
        else:
            m, n = witness
    except Exception:
        return [False, False]
    
    # H_1: m is a positive integer
    try:
        h1_ok = bool(isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool) and m > 0)
    except Exception:
        h1_ok = False

    # neg_Q: \lambda(mn) != \lambda(m)\lambda(n)
    # If n is not a positive integer, the Liouville function is undefined,
    # meaning the equation fails to hold (hence neg_Q is True).
    try:
        L_mn = liouville(m * n)
        L_m = liouville(m)
        L_n = liouville(n)
        q = (L_mn == L_m * L_n)
        neg_q = not q
    except Exception:
        # The conclusion fails because the function is applied outside its domain
        neg_q = True

    return [h1_ok, neg_q]