import sympy
from sympy import factorint, totient

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    
    The witness should be a tuple (n, k).
    Hypotheses:
      - k is the number of distinct odd prime factors of n
    Conclusion:
      - 2^k divides phi(n)
    """
    try:
        n, k = witness
    except Exception:
        return [False, False]

    # H_1: k is the number of distinct odd prime factors of n
    try:
        # factorint returns a dictionary of prime factors and their multiplicities.
        # We count the number of distinct prime factors that are odd (and > 0 to exclude -1 if n is negative).
        factors = factorint(n)
        actual_k = sum(1 for p in factors if p > 2 and p % 2 != 0 and sympy.isprime(p))
        h1_ok = (k == actual_k)
    except Exception:
        h1_ok = False

    # neg_Q: 2^k does NOT divide phi(n)
    try:
        phi_n = totient(n)
        # The conclusion is that 2^k divides phi(n).
        # We want the negation: 2^k does NOT divide phi(n).
        neg_q = (phi_n % (2**k)) != 0
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: k is the number of distinct odd prime factors of n",
    "¬Q: 2^k does not divide phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1