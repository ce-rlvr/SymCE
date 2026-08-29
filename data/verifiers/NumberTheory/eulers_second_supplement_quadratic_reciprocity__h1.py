import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        h1 = (p > 2)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p <= 0:
            neg_q = False
        else:
            has_root = False
            # Limit iterations to prevent timeout on unreasonably large witnesses
            limit = min(p, 1000000)
            for x in range(limit):
                if (x * x) % p == 2 % p:
                    has_root = True
                    break
            
            mod_cond = (p % 8 == 1) or (p % 8 == 7)
            neg_q = (has_root != mod_cond)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p > 2",
    "¬Q: (exists x: x^2 = 2 mod p) is not equivalent to (p = 1 mod 8 or p = 7 mod 8)"
]

N_HYP = 1
NEG_Q_INDEX = 1