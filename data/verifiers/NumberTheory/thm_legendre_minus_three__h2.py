import sympy
import sympy.ntheory

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p != witness:
            h1 = False
        else:
            h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p != witness:
            q_ok = False
        else:
            # The conclusion states implications for p = 1 (mod 3) and p = 2 (mod 3).
            # If p = 2, legendre_symbol raises a ValueError (as it is only defined for odd primes),
            # which will be caught by the except block, correctly marking the conclusion as False.
            if p % 3 == 1:
                q_ok = (sympy.ntheory.legendre_symbol(-3, p) == 1)
            elif p % 3 == 2:
                q_ok = (sympy.ntheory.legendre_symbol(-3, p) == -1)
            else:
                q_ok = True
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The Legendre symbol (-3/p) does not match the expected value or is undefined"
]

N_HYP = 1
NEG_Q_INDEX = 1