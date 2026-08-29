import sympy
import math

def conditions(witness):
    try:
        h1 = (int(witness) == witness) and (witness > 0)
    except Exception:
        h1 = False

    # The second hypothesis is a definitional statement about the notation \phi(k).
    # It is unconditionally true in the context of this verifier.
    h2 = True

    try:
        n = witness
        lhs = sum(sympy.totient(k) * math.floor(n / k) for k in range(1, int(n) + 1))
        rhs = sympy.Rational(n * (n + 1), 2)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: \phi(k) is Euler's totient function",
    "¬Q: \sum_{k=1}^{n} \phi(k) \lfloor n/k \rfloor \neq n(n+1)/2"
]

N_HYP = 2
NEG_Q_INDEX = 2