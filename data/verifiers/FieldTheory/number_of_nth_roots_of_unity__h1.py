import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Given a witness (n, q), checks if it is a valid counterexample to the false conjecture.
    The conjecture claims that for any q, the number of solutions to x^n = 1 in F_q 
    (interpreted here as Z/qZ since the prime power hypothesis is dropped) is gcd(n, q-1).
    """
    try:
        # Unpack witness. It can be a dict, an object with attributes, or a tuple.
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
        elif hasattr(witness, 'n') and hasattr(witness, 'q'):
            n = witness.n
            q = witness.q
        else:
            n, q = witness
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val > 0)
    except Exception:
        h1 = False

    # ¬Q: The number of elements x in F_q satisfying x^n = 1 is NOT exactly gcd(n, q-1)
    # Since the "q is a prime power" hypothesis was dropped, F_q is evaluated as the ring Z/qZ.
    try:
        q_val = int(q)
        if q_val == q and q_val > 1:
            # Count solutions to x^n = 1 mod q
            count = sum(1 for i in range(q_val) if pow(i, n_val, q_val) == 1)
            expected_count = math.gcd(n_val, q_val - 1)
            neg_q = (count != expected_count)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The number of elements x in F_q satisfying x^n = 1 is not exactly gcd(n, q-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1