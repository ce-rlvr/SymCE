import sympy
import math

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n >= 1) and (n == witness)
    except Exception:
        h1 = False

    # neg_Q: The modular inverse of 3 modulo n is NOT congruent to (n(3 - (n \bmod 3)) + 1) / 3 \pmod n
    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            formula = (n * (3 - (n % 3)) + 1) // 3
            try:
                inv = pow(3, -1, n)
                holds = (inv % n) == (formula % n)
            except ValueError:
                # Modular inverse does not exist
                holds = False
            neg_q = not holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The modular inverse of 3 modulo n is not congruent to (n(3 - (n mod 3)) + 1) / 3 mod n (or does not exist)"
]

N_HYP = 1
NEG_Q_INDEX = 1