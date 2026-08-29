import sympy
import math
from sympy.abc import x

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to provide the characteristic p and the integer n.
    It can be a tuple/list (p, n), a dict {'p': p, 'n': n}, or just n (assuming p=0).
    """
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            n = int(witness['n'])
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            p = int(witness[0])
            n = int(witness[1])
        else:
            n = int(witness)
            p = 0
    except Exception:
        return [False, False, False]

    # H_1: K is an algebraically closed field of characteristic p >= 0
    # This means p must be 0 or a prime number.
    try:
        h1_ok = bool((p == 0) or sympy.isprime(p))
    except Exception:
        h1_ok = False

    # H_2: If p > 0, then n is coprime to p
    try:
        if p > 0:
            h2_ok = bool(math.gcd(n, p) == 1)
        else:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The polynomial x^n - 1 does not have exactly n distinct roots in K.
    # If n > 0, since gcd(n, p) == 1 (or p=0), the derivative is nx^{n-1} != 0,
    # so x^n - 1 has no multiple roots and thus exactly n distinct roots in the algebraically closed field K.
    # If n == 0, x^0 - 1 = 0, which has infinitely many roots (not exactly 0).
    # If n < 0, x^n - 1 is not a polynomial, so the statement fails.
    # Therefore, the conclusion fails (neg_q_ok is True) if and only if n <= 0.
    try:
        neg_q_ok = not (n > 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field of characteristic p >= 0",
    "H_2: If p > 0, then n is coprime to p",
    "¬Q: The polynomial x^n - 1 does not have exactly n distinct roots in K"
]

N_HYP = 2
NEG_Q_INDEX = 2