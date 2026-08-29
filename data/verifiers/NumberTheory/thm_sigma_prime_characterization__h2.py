import sympy
from sympy.ntheory import isprime

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        is_int = isinstance(witness, (int, sympy.Integer))
        h1_ok = bool(is_int and witness > 1)
    except Exception:
        h1_ok = False

    try:
        is_int = isinstance(witness, (int, sympy.Integer))
        if is_int:
            neg_q_ok = not isprime(witness)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: n is not a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1