import sympy

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if all(isinstance(x, (int, sympy.Integer)) for x in (a, b, c)):
            if a > 0 and b > 0 and c > 0:
                h1 = True
    except Exception:
        h1 = False

    try:
        h2 = bool(a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    try:
        neg_q = bool((a % 4 == 0) == (b % 4 == 0))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: It is not the case that exactly one of a or b is divisible by 4"
]

N_HYP = 2
NEG_Q_INDEX = 2