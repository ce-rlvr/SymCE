import math
from sympy import isprime

def conditions(witness) -> list[bool]:
    # H_1: n is an integer
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n == witness)
    except Exception:
        h1 = False

    # neg_Q: n and n+2 are twin primes iff 4((n-1)! + 1) + n == 0 mod n(n+2)
    try:
        n = int(witness)
        P = isprime(n) and isprime(n + 2)
        fact = math.factorial(n - 1)
        modulus = n * (n + 2)
        if modulus == 0:
            Q = False
        else:
            Q = (4 * (fact + 1) + n) % modulus == 0
        neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: (n and n+2 are twin primes) is not equivalent to (4((n-1)! + 1) + n ≡ 0 mod n(n+2))"
]

N_HYP = 1
NEG_Q_INDEX = 1