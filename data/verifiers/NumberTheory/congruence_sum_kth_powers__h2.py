import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p_val = witness['p']
            k_val = witness['k']
        elif hasattr(witness, 'p') and hasattr(witness, 'k'):
            p_val = witness.p
            k_val = witness.k
        else:
            p_val, k_val = witness
            
        if not isinstance(p_val, (int, sympy.Integer)) or isinstance(p_val, bool):
            return [False, False, False]
        if not isinstance(k_val, (int, sympy.Integer)) or isinstance(k_val, bool):
            return [False, False, False]
            
        p = int(p_val)
        k = int(k_val)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    try:
        if p > 1:
            h2 = bool((k % (p - 1)) != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if p > 1:
            total = sum(pow(x, k, p) for x in range(1, p))
            neg_q = bool((total % p) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k is not a multiple of p-1",
    "¬Q: sum_{x=1}^{p-1} x^k is not congruent to 0 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2