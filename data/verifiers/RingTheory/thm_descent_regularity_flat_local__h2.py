import sympy
from sympy.ntheory import factorint, isprime
from sympy.abc import x, y, z

# Top-level setup
# Witness should be a tuple of two integers (n_R, n_S) representing the rings Z/n_R Z and Z/n_S Z.
# Z/nZ is a Noetherian local ring iff n = p^k for some prime p and k >= 1.
# It is a regular local ring iff k = 1 (i.e., n is prime).

def is_noetherian_local(n):
    try:
        n = int(n)
        if n <= 1:
            return False
        factors = factorint(n)
        return len(factors) == 1
    except Exception:
        return False

def is_regular_local(n):
    try:
        n = int(n)
        if not is_noetherian_local(n):
            return False
        return isprime(n)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        R, S = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(is_noetherian_local(R) and is_noetherian_local(S))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_regular_local(S))
    except Exception:
        h2 = False

    try:
        neg_q = not bool(is_regular_local(R))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are Noetherian local rings",
    "H_2: S is a regular local ring",
    "¬Q: R is not a regular local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2