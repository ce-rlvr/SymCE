import sympy
import math
from sympy.ntheory import divisors

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

    # neg_Q: \prod_{d|n} d \neq n^{d(n)/2}
    try:
        if isinstance(witness, bool):
            neg_q = False
        else:
            n = int(witness)
            if n <= 0 or n != witness:
                neg_q = False
            else:
                divs = divisors(n)
                prod = 1
                for d in divs:
                    prod *= d
                
                # We check prod**2 != n**d(n) to avoid floating point issues with fractional exponents
                lhs = prod ** 2
                rhs = n ** len(divs)
                neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: product of divisors of n is not equal to n^{d(n)/2}"
]

N_HYP = 1
NEG_Q_INDEX = 1