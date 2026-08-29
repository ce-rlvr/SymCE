import sympy
from sympy.ntheory import isprime, divisor_sigma, totient

def conditions(witness) -> list[bool]:
    try:
        n = sympy.sympify(witness)
        if not n.is_integer:
            h1 = False
        else:
            h1 = bool(isprime(n))
    except Exception:
        h1 = False

    try:
        n = sympy.sympify(witness)
        if not n.is_integer:
            neg_q = False
        else:
            neg_q = bool(divisor_sigma(n) + totient(n) != 2 * n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a prime number",
    "¬Q: sigma(n) + phi(n) != 2n"
]

N_HYP = 1
NEG_Q_INDEX = 1