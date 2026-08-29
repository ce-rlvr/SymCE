import sympy
import sympy.ntheory
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p', 2)
            M_p = witness.get('M_p', 2**p - 1)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                p, M_p = witness
            else:
                p = witness[0]
                M_p = 2**p - 1
        else:
            p = witness
            M_p = 2**p - 1
        
        p = int(p)
        M_p = int(M_p)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = bool(M_p == (2**p - 1))
    except Exception:
        h2 = False

    try:
        # Safeguard against extremely large numbers hanging the totient function
        if p > 500:
            neg_q = False
        else:
            neg_q = bool(sympy.ntheory.totient(M_p) != (2**p - 2))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: M_p = 2^p - 1",
    "¬Q: phi(M_p) != 2^p - 2"
]

N_HYP = 2
NEG_Q_INDEX = 2