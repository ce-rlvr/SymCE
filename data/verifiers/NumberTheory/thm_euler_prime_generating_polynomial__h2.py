import sympy
from sympy.ntheory import isprime

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    Returns [H_1, neg_Q]
    """
    # H_1: n is an integer
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool)
    except Exception:
        h1 = False

    # ¬Q: f(n) = n^2 + n + 41 is not prime
    try:
        if h1:
            n = int(witness)
            val = n**2 + n + 41
            neg_q = not isprime(val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: f(n) = n^2 + n + 41 is not prime"
]

N_HYP = 1
NEG_Q_INDEX = 1