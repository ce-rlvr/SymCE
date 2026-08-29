import math
from sympy import Integer

# Top-level setup
# No named bindings needed for this number theory domain; use integers directly.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            m = witness.get('m')
        else:
            a, b, c, m = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(a, (int, Integer)) and isinstance(b, (int, Integer)) and \
             isinstance(c, (int, Integer)) and isinstance(m, (int, Integer)) and m > 0
    except Exception:
        h1 = False

    try:
        h2 = ((a * c) - (b * c)) % m == 0
    except Exception:
        h2 = False

    try:
        neg_q = (a - b) % m != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, c, and m are integers with m > 0",
    "H_2: ac ≡ bc (mod m)",
    "¬Q: a ≢ b (mod m)"
]

N_HYP = 2
NEG_Q_INDEX = 2