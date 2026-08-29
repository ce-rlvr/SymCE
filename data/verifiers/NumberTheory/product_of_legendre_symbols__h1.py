import sympy
from sympy.ntheory import jacobi_symbol

# No specific top-level bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        prod = 1
        for a in range(1, p):
            prod *= jacobi_symbol(a, p)
        
        rhs = sympy.S(-1)**sympy.Rational(p - 1, 2)
        neg_q = bool(prod != rhs)
    except Exception:
        # If jacobi_symbol is undefined (e.g., p is even) or another error occurs,
        # the conclusion formula fails to hold.
        neg_q = True

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The product of Legendre symbols mod p does not equal (-1)^((p-1)/2)"
]

N_HYP = 0
NEG_Q_INDEX = 0