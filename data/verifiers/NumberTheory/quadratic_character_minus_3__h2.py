import sympy
from sympy.ntheory import isprime, legendre_symbol

def conditions(witness):
    try:
        p = int(witness)
    except Exception:
        return [False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        q_holds = True
        if p % 3 == 1:
            if legendre_symbol(-3, p) != 1:
                q_holds = False
        elif p % 3 == 2:
            if legendre_symbol(-3, p) != -1:
                q_holds = False
    except Exception:
        # If legendre_symbol is undefined (e.g., for p=2), the conclusion fails.
        q_holds = False

    neg_q = not q_holds

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "¬Q: The conclusion about the Legendre symbol (-3/p) fails or is undefined"
]

N_HYP = 1
NEG_Q_INDEX = 1