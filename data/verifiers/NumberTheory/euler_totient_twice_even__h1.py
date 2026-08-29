import sympy
from sympy.ntheory import totient

# Top-level setup
# No specific named objects are required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    # H_1: n is an even integer
    try:
        n = sympy.S(witness)
        if n.is_integer is True:
            h1 = bool(n % 2 == 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: phi(2n) != 2*phi(n)
    try:
        n = sympy.S(witness)
        if n.is_integer is True:
            n = int(n)
        
        # If totient is undefined (e.g., for n <= 0), this will raise an exception.
        lhs = totient(2 * n)
        rhs = 2 * totient(n)
        neg_q = bool(lhs != rhs)
    except Exception:
        # If evaluating the conclusion raises an exception, the conclusion fails.
        # Therefore, the negation of the conclusion is True.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an even integer",
    "¬Q: phi(2n) != 2*phi(n) or is undefined"
]

N_HYP = 1
NEG_Q_INDEX = 1