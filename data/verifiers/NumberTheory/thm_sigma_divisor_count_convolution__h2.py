import sympy
from sympy.ntheory import divisor_sigma, divisor_count, divisors

# No specific top-level setup needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        h1 = isinstance(witness, int) and not isinstance(witness, bool) and witness > 0
    except Exception:
        h1 = False

    # H_2: d(n) denotes the number of divisors function (definitional, always true)
    try:
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: \sum_{k|n} \sigma(k) != \sum_{k|n} \frac{n}{k} d(k)
    try:
        if h1:
            n = witness
            divs = divisors(n)
            lhs = sum(divisor_sigma(k) for k in divs)
            rhs = sum((n // k) * divisor_count(k) for k in divs)
            neg_q = bool(lhs != rhs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: d(n) denotes the number of divisors function",
    "¬Q: sum_{k|n} sigma(k) != sum_{k|n} (n/k) d(k)"
]

N_HYP = 2
NEG_Q_INDEX = 2