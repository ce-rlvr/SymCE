import sympy
from sympy import isprime
from sympy.ntheory import legendre_symbol

# Top-level setup
# No specific named bindings needed for this number theory problem; integers are used directly.

def conditions(witness) -> list[bool]:
    try:
        p = int(sympy.sympify(witness))
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        p = int(sympy.sympify(witness))
        l = legendre_symbol(3, p)
        
        if p % 12 in (1, 11):
            q_ok = (l == 1)
        elif p % 12 in (5, 7):
            q_ok = (l == -1)
        else:
            # If p % 12 is not in the above cases, the piecewise formula 
            # fails to correctly describe the Legendre symbol (3/p).
            q_ok = False
    except Exception:
        # If legendre_symbol raises an error (e.g., for p=2), the conclusion fails.
        q_ok = False

    neg_q = not q_ok

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "¬Q: (3/p) != 1 for p = +/-1 mod 12, or (3/p) != -1 for p = +/-5 mod 12"
]

N_HYP = 1
NEG_Q_INDEX = 1