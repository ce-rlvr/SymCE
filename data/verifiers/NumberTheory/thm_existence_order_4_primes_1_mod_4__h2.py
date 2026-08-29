import sympy
import sympy.ntheory
import math

# Top-level setup
# (No specific bindings needed for this number theory problem)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # H_1: p is a prime number
    try:
        h1_ok = bool(sympy.isprime(witness))
    except Exception:
        h1_ok = False

    # ¬Q: There does NOT exist an integer a such that the multiplicative order of a modulo p is exactly 4
    try:
        p = int(witness)
        if p >= 2:
            # The maximal multiplicative order modulo p is given by the Carmichael function (reduced_totient).
            # An element of order 4 exists modulo p if and only if 4 divides this maximal order.
            has_order_4 = (sympy.reduced_totient(p) % 4 == 0)
            neg_q_ok = not has_order_4
        else:
            # For p < 2, the multiplicative group modulo p does not contain an element of order 4.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: There does not exist an integer a such that the multiplicative order of a modulo p is exactly 4"
]

N_HYP = 1
NEG_Q_INDEX = 1