import math
import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        h1 = isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer)
        h1 = bool(h1)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        sum_coprime = sum(i for i in range(1, n) if math.gcd(i, n) == 1)
        phi_n = totient(n)
        neg_q = (2 * sum_coprime != n * phi_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: The sum of positive integers less than n and coprime to n is not equal to 1/2 n phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1