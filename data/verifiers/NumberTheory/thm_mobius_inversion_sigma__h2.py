import sympy
from sympy.ntheory import divisors, divisor_sigma, mobius

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    # ¬Q: \sum_{d|n} \sigma(d) \mu(n/d) != n
    try:
        if isinstance(witness, (int, sympy.Integer)) and witness > 0:
            n = int(witness)
            lhs = sum(divisor_sigma(d) * mobius(n // d) for d in divisors(n))
            neg_q = bool(lhs != n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sum_{d|n} sigma(d) mu(n/d) != n"
]

N_HYP = 1
NEG_Q_INDEX = 1