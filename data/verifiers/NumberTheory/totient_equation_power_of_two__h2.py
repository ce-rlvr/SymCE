import sympy
import math

# Top-level setup
# (No named bindings required for this number theory domain)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, int) and witness > 0
    except Exception:
        h1 = False

    try:
        is_power_of_two_pos_k = isinstance(witness, int) and witness > 1 and (witness & (witness - 1)) == 0
        neg_q = not is_power_of_two_pos_k
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: n is not 2^k for some positive integer k"
]

N_HYP = 1
NEG_Q_INDEX = 1