import sympy
import math

def conditions(witness):
    try:
        p = int(witness)
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p < 2:
            neg_q = False
        else:
            p2 = p**2
            total = 0
            for i in range(1, p):
                inv = pow(i, -1, p2)
                total = (total + inv) % p2
            neg_q = (total != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: \\sum_{i=1}^{p-1} i^{-1} \\not\\equiv 0 \\pmod{p^2}"
]

N_HYP = 1
NEG_Q_INDEX = 1