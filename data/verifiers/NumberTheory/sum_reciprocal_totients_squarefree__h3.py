import sympy
from sympy.ntheory import divisors, mobius, totient

# Top-level setup (none needed for this domain)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            h1 = False
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = bool(witness > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2 is definitional
    h2 = True

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            lhs = sum(sympy.Rational(mobius(d)**2, totient(d)) for d in divisors(n))
            rhs = sympy.Rational(n, totient(n))
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: mu(n) is the Mobius function",
    "¬Q: sum_{d|n} mu^2(d)/phi(d) != n/phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2