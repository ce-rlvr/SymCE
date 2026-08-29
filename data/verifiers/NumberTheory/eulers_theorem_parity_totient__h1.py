import sympy
from sympy.ntheory import totient

# Top-level setup
# (No specific named bindings are required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    # H_1: n >= 3
    try:
        h1 = bool(witness >= 3)
    except Exception:
        h1 = False

    # ¬Q: phi(n) is not an even integer
    try:
        phi_n = totient(witness)
        val = int(phi_n)
        neg_q = bool(val % 2 != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3",
    "¬Q: phi(n) is not an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1