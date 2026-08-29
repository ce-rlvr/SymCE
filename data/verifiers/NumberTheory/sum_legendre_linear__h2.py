import sympy
from sympy.ntheory import isprime, legendre_symbol

# Top-level setup
# No specific named objects required for this number theory conjecture

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (p, a, b), checks if it satisfies the hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        p, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime
    try:
        h1_ok = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1_ok = False

    # H_2: p does not divide a
    try:
        h2_ok = bool(a % p != 0)
    except Exception:
        h2_ok = False

    # neg_Q: The sum of Legendre symbols is not 0
    try:
        total_sum = sum(legendre_symbol(a * x + b, p) for x in range(int(p)))
        neg_q_ok = bool(total_sum != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: p does not divide a",
    "¬Q: sum of Legendre symbols is not 0"
]

N_HYP = 2
NEG_Q_INDEX = 2