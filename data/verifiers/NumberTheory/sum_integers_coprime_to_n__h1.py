import math
import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        n = int(witness)
        h1 = (n == witness) and (n >= 1)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        s = sum(k for k in range(1, n + 1) if math.gcd(k, n) == 1)
        rhs = sympy.Rational(n * totient(n), 2)
        neg_q = bool(s != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer >= 1",
    "¬Q: sum_{1 <= k <= n, gcd(k,n)=1} k != n * phi(n) / 2"
]

N_HYP = 1
NEG_Q_INDEX = 1