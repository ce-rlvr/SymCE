import sympy
from sympy import mobius, totient, divisors, Rational

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    try:
        # The second hypothesis simply establishes notation for the Möbius function.
        # It is vacuously true for any witness in this context.
        h2 = True
    except Exception:
        h2 = False

    try:
        if h1:
            n = int(witness)
            lhs = sum(Rational(mobius(d), d) for d in divisors(n))
            rhs = Rational(totient(n), n)
            neg_q = bool(lhs != rhs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: mu(n) is the Möbius function",
    "¬Q: sum_{d|n} mu(d)/d != phi(n)/n"
]

N_HYP = 2
NEG_Q_INDEX = 2