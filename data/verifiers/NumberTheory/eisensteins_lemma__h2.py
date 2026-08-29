import sympy
from sympy.ntheory import isprime, legendre_symbol

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        p, a = witness
    except Exception:
        return [False, False, False]

    try:
        p = int(p)
        a = int(a)
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime
    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # H_2: a is not divisible by p
    try:
        h2 = bool(a % p != 0)
    except Exception:
        h2 = False

    # neg_Q: The Legendre symbol (a/p) is NOT equal to (-1)^S
    try:
        if not (isprime(p) and p % 2 != 0):
            neg_q = False
        else:
            S = sum((u * a) // p for u in range(1, (p - 1) // 2 + 1))
            lhs = legendre_symbol(a, p)
            rhs = (-1) ** S
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is not divisible by p",
    "¬Q: The Legendre symbol (a/p) is not equal to (-1)^S"
]

N_HYP = 2
NEG_Q_INDEX = 2