import math
import sympy
from sympy.ntheory import isprime, divisor_sigma

# Top-level setup
# No special named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - n is a composite number
    
    Conclusion (must FAIL at the witness):
      sigma(n) > n + sqrt(n)
    """
    # H_1: n is a composite number
    try:
        # A composite number is a positive integer greater than 1 that is not prime.
        n = int(witness)
        h1_ok = (n > 1) and not isprime(n)
    except Exception:
        h1_ok = False

    # neg_Q: sigma(n) <= n + sqrt(n)
    try:
        n = int(witness)
        if n >= 0:
            sigma_n = divisor_sigma(n)
            sqrt_n = math.sqrt(n)
            neg_q_ok = bool(sigma_n <= n + sqrt_n)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a composite number",
    "¬Q: sigma(n) <= n + sqrt(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1