import sympy
from sympy.ntheory import totient, primefactors

def conditions(witness) -> list[bool]:
    try:
        h1 = (isinstance(witness, int) and not isinstance(witness, bool)) or isinstance(witness, sympy.Integer)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            phi_n = totient(n)
            factors = primefactors(n)
            prod = sympy.Rational(1, 1)
            for p in factors:
                prod *= (1 - sympy.Rational(1, p))
            rhs = n * prod
            neg_q = bool(phi_n != rhs)
    except Exception:
        # If primefactors(n) raises an error (e.g., for n=0), the formula is undefined,
        # so the equality fails.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: phi(n) != n * prod_{p|n} (1 - 1/p)"
]

N_HYP = 1
NEG_Q_INDEX = 1