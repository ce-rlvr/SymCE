import sympy
from sympy.ntheory import divisors

def conditions(witness):
    try:
        n = int(witness)
        if n <= 0:
            h1_ok = False
        else:
            h1_ok = sum(divisors(n)) == 2 * n
    except Exception:
        h1_ok = False

    try:
        n = int(witness)
        neg_q_ok = (n % 10) not in (6, 8)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a perfect number",
    "¬Q: n is not congruent to 6 or 8 mod 10"
]

N_HYP = 1
NEG_Q_INDEX = 1