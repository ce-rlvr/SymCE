import math

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, b, n), checks if it is a valid counterexample to the false conjecture.
    The conjecture states that for positive integers a > b, if the Euclidean algorithm
    requires n division steps to compute gcd(a, b), then n <= 5 * d, where d is the number
    of decimal digits of b.
    
    Wait, Lamé's theorem is actually ALWAYS true for the standard Euclidean algorithm.
    However, the prompt implies there is a counterexample. We will evaluate the conditions
    exactly as specified.
    """
    try:
        a, b, n = witness
    except Exception:
        return [False, False, False]

    # H1: a and b are positive integers with a > b
    try:
        h1_ok = isinstance(a, int) and isinstance(b, int) and a > b > 0
    except Exception:
        h1_ok = False

    # H2: The Euclidean algorithm requires n division steps to compute the greatest common divisor of a and b
    try:
        if not h1_ok:
            h2_ok = False
        else:
            steps = 0
            x, y = a, b
            while y != 0:
                x, y = y, x % y
                steps += 1
            h2_ok = (steps == n)
    except Exception:
        h2_ok = False

    # neg_Q: n > 5d, meaning the number of steps is MORE than five times the number of decimal digits of b
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            d = len(str(b))
            neg_q_ok = n > 5 * d
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a and b are positive integers with a > b",
    "H_2: The Euclidean algorithm requires n division steps to compute the greatest common divisor of a and b",
    "¬Q: n > 5d (the number of steps is more than five times the number of decimal digits of b)"
]

N_HYP = 2
NEG_Q_INDEX = 2