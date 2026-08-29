import sympy
from sympy.ntheory import totient, divisor_sigma, isprime

# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    # H_1: n is an integer
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool)
    except Exception:
        h1 = False

    # ¬Q: phi(n) + sigma(n) < 2n or equality does not hold if and only if n is prime
    try:
        n = int(witness)
        phi = totient(n)
        sigma = divisor_sigma(n)
        
        q1 = (phi + sigma >= 2 * n)
        q2 = ((phi + sigma == 2 * n) == isprime(n))
        
        neg_q = not (q1 and q2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: phi(n) + sigma(n) < 2n or equality does not hold if and only if n is prime"
]

N_HYP = 1
NEG_Q_INDEX = 1