import sympy
import sympy.ntheory
import math

def liouville(n):
    factors = sympy.ntheory.factorint(n)
    omega = sum(factors.values())
    return (-1) ** omega

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n == witness) and (n > 0)
    except Exception:
        h1 = False

    # ¬Q: \sum_{d|n} \lambda(d) != 1 if n is a perfect square, and 0 otherwise
    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            divs = sympy.ntheory.divisors(n)
            sum_lambda = sum(liouville(d) for d in divs)
            
            is_perfect_square = (math.isqrt(n)**2 == n)
            expected = 1 if is_perfect_square else 0
            
            neg_q = bool(sum_lambda != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sum_{d|n} lambda(d) != 1 if n is a perfect square, and 0 otherwise"
]

N_HYP = 1
NEG_Q_INDEX = 1