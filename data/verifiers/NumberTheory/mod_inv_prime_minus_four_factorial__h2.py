import sympy
import math

def conditions(witness):
    try:
        h1 = bool(sympy.isprime(witness))
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p < 4:
            neg_q = True
        else:
            f = math.factorial(p - 4)
            inv = sympy.mod_inverse(f, p)
            neg_q = bool((inv % p) != (6 % p))
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The modular inverse of (p - 4)! modulo p is not congruent to 6 (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1