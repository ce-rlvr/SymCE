import sympy
import sympy.ntheory

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
    except Exception:
        h1 = False

    try:
        neg_q = sympy.ntheory.totient(m * n) != sympy.ntheory.totient(m) * sympy.ntheory.totient(n)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: phi(mn) != phi(m)phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1