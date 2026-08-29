import math
import sympy

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The product of all positive divisors of n is not equal to n^{d(n)/2}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, str):
            h1 = False
        else:
            n = int(witness)
            h1 = (n == witness) and (n > 0)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            divs = sympy.divisors(n)
            d = len(divs)
            prod = 1
            for div in divs:
                prod *= div
            
            if d % 2 == 0:
                expected = n ** (d // 2)
                neg_q = bool(prod != expected)
            else:
                root = math.isqrt(n)
                if root * root == n:
                    expected = (n ** (d // 2)) * root
                    neg_q = bool(prod != expected)
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]