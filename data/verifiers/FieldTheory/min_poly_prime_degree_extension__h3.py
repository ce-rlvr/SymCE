import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p', 0)
            d = witness.get('d', 0)
        else:
            p, d = witness
        h1 = isinstance(p, int) and isinstance(d, int) and p >= 1 and d >= 1
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            p = witness.get('p', 0)
        else:
            p, d = witness
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            p = witness.get('p', 0)
            d = witness.get('d', 0)
        else:
            p, d = witness
        neg_q = bool(d != 1 and d != p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E over F is a field extension and alpha has a minimal polynomial",
    "H_2: The degree of E over F is a prime number p",
    "¬Q: The degree of the minimal polynomial of alpha over F is neither 1 nor p"
]

N_HYP = 2
NEG_Q_INDEX = 2