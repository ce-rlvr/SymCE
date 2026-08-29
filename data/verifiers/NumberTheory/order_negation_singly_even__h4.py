import sympy
import sympy.ntheory
import math

# No specific top-level setup needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            a = int(witness['a'])
            d = int(witness['d'])
        else:
            p = int(witness[0])
            a = int(witness[1])
            d = int(witness[2])
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(math.gcd(a, p) == 1)
    except Exception:
        h2 = False

    try:
        a_mod = a % p
        h3 = bool(sympy.ntheory.n_order(a_mod, p) == d)
    except Exception:
        h3 = False

    try:
        neg_a_mod = (-a) % p
        order_neg_a = sympy.ntheory.n_order(neg_a_mod, p)
        neg_q = bool(order_neg_a != d / 2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: a is an integer coprime to p",
    "H_3: The multiplicative order of a modulo p is d",
    "¬Q: The multiplicative order of -a modulo p is not d/2"
]

N_HYP = 3
NEG_Q_INDEX = 3