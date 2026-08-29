import sympy
from sympy.ntheory import isprime

# Top-level setup
# No special named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Given a witness (m, p), checks the remaining hypotheses and the negated conclusion.
    """
    try:
        m, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F_m = 2^{2^m} + 1
    # We just compute F_m. If m is not an integer or m < 0, this might not be an integer.
    try:
        if not isinstance(m, int) or m < 0:
            # If m is negative, 2^m is a fraction, so 2^{2^m} is not an integer.
            # We'll allow it if it somehow evaluates to an integer, but typically it won't.
            F_m = 2**(2**m) + 1
        else:
            F_m = 2**(2**m) + 1
        # Check if F_m is an integer
        h1_ok = (F_m == int(F_m))
        F_m = int(F_m)
    except Exception:
        h1_ok = False

    # H_2: p is a prime number
    try:
        h2_ok = bool(isprime(p))
    except Exception:
        h2_ok = False

    # H_3: p divides F_m
    try:
        if h1_ok and h2_ok:
            h3_ok = (F_m % p == 0)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: The multiplicative order of 2 modulo p is NOT 2^{m+1}
    try:
        if h2_ok and p > 1:
            # Compute the multiplicative order of 2 modulo p
            # Since p is prime, we can use sympy's n_order
            order = sympy.ntheory.n_order(2, p)
            expected_order = 2**(m + 1)
            neg_q_ok = (order != expected_order)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_m = 2^{2^m} + 1 is an integer",
    "H_2: p is a prime number",
    "H_3: p divides F_m",
    "¬Q: The multiplicative order of 2 modulo p is not 2^{m+1}"
]

N_HYP = 3
NEG_Q_INDEX = 3