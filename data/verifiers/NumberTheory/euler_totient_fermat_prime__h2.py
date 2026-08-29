import sympy
from sympy import totient, isprime

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            k = witness.get('k')
            F_k = witness.get('F_k')
        elif hasattr(witness, 'k') and hasattr(witness, 'F_k'):
            k = witness.k
            F_k = witness.F_k
        else:
            k, F_k = witness
    except Exception:
        return [False, False, False]

    # H_1: k is a non-negative integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and k >= 0
    except Exception:
        h1 = False

    # H_2: F_k is a prime number
    try:
        h2 = bool(isprime(F_k))
    except Exception:
        h2 = False

    # neg_Q: phi(F_k) != 2^(2^k)
    try:
        if k < 0 or k > 15:
            neg_q = False
        else:
            neg_q = bool(totient(F_k) != 2**(2**k))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: k is a non-negative integer",
    "H_2: F_k is a prime number",
    "¬Q: phi(F_k) != 2**(2**k)"
]

N_HYP = 2
NEG_Q_INDEX = 2