import sympy
from sympy.ntheory import totient

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        # Check if witness is an integer greater than 1
        h1_ok = bool(p > 1 and p == witness)
    except Exception:
        h1_ok = False

    try:
        p = int(witness)
        if p == witness and p > 1:
            # The multiplicative group of units modulo p has order totient(p).
            # For it to be a cyclic group of order p-1, its order must be p-1
            # (which also implies p is prime and the group is cyclic).
            order = totient(p)
            neg_q_ok = bool(order != p - 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an integer > 1",
    "¬Q: (Z/pZ)^x is not a cyclic group of order p-1"
]

N_HYP = 1
NEG_Q_INDEX = 1