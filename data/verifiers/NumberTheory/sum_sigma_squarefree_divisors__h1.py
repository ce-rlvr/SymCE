import sympy
from sympy.ntheory import divisors, mobius, divisor_sigma, primefactors

def conditions(witness):
    try:
        n = int(witness)
        if n < 1:
            return [False]
    except Exception:
        return [False]

    try:
        lhs = sum((mobius(d)**2) * divisor_sigma(d) for d in divisors(n))
        rhs = 1
        for p in primefactors(n):
            rhs *= (p + 2)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum_{d|n} mu^2(d) sigma(d) != prod_{p|n} (p+2)"
]

N_HYP = 0
NEG_Q_INDEX = 0