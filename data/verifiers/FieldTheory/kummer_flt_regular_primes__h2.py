import sympy
from sympy import bernoulli, isprime

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (p, x, y, z), checks if it satisfies the remaining 
    hypotheses and falsifies the conclusion.
    """
    try:
        p, x, y, z = witness
    except Exception:
        return [False, False]

    # H_1: p >= 3 is a regular prime
    try:
        h1 = False
        if isinstance(p, int) and p >= 3 and isprime(p):
            h1 = True
            # Kummer's criterion for regular primes:
            # p does not divide the numerator of Bernoulli numbers B_k for even k in [2, p-3]
            for k in range(2, p - 2, 2):
                b = bernoulli(k)
                if b.p % p == 0:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: The product xyz is not equal to 0
    try:
        neg_q = (x * y * z != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p >= 3 is a regular prime",
    "¬Q: The product xyz is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1