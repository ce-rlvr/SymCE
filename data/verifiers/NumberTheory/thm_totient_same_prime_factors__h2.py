import sympy
from sympy.ntheory import totient

# Top-level setup (no named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool) and 
              isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and 
              m > 0 and n > 0)
    except Exception:
        h1 = False

    try:
        neg_q = bool(m * totient(n) != n * totient(m))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: m * phi(n) != n * phi(m)"
]

N_HYP = 1
NEG_Q_INDEX = 1