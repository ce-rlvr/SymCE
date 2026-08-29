import sympy
from sympy import gcd

# Top-level setup
# No specific named objects needed for this number theory / ring theory conjecture.
# We will use integers as the UFD R = Z.

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, b, n, m), checks:
      H_1: R is a UFD (implicitly True for Z)
      H_2: gcd(a, b) is a unit in R (i.e., gcd(a, b) == 1 in Z)
      H_3: n and m are positive integers
      neg_Q: gcd(a^n, b^m) is NOT a unit in R (i.e., gcd(a^n, b^m) != 1 in Z)
    """
    try:
        a, b, n, m = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R is a UFD
    # We are working in Z, which is a UFD.
    h1_ok = True

    # H_2: gcd(a, b) is a unit in R
    try:
        if not (isinstance(a, int) and isinstance(b, int)):
            h2_ok = False
        else:
            h2_ok = (gcd(a, b) == 1)
    except Exception:
        h2_ok = False

    # H_3: n and m are positive integers
    try:
        h3_ok = isinstance(n, int) and isinstance(m, int) and n > 0 and m > 0
    except Exception:
        h3_ok = False

    # neg_Q: gcd(a^n, b^m) is NOT a unit in R
    try:
        if not (isinstance(a, int) and isinstance(b, int) and isinstance(n, int) and isinstance(m, int)):
            neg_q_ok = False
        else:
            # We must be careful with large powers, but since n, m are positive integers,
            # we can compute gcd(a^n, b^m).
            # To avoid huge numbers, we can just check if gcd(a, b) == 1,
            # but we must evaluate the actual conclusion.
            # Actually, gcd(a^n, b^m) == 1 iff gcd(a, b) == 1.
            # So neg_q_ok will be True if gcd(a^n, b^m) != 1.
            val_gcd = gcd(a**n, b**m)
            neg_q_ok = (val_gcd != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: The greatest common divisor of a and b is a unit in R",
    "H_3: n and m are positive integers",
    "¬Q: The greatest common divisor of a^n and b^m is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3