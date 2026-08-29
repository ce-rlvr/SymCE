import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(sympy.gcd(a, b) == 1)
    except Exception:
        h1_ok = False

    try:
        q_ok = bool(sympy.gcd(a + b, a * b) == 1)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a and b are coprime",
    "¬Q: gcd(a+b, ab) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1