import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p <= 1:
            return [False]
    except Exception:
        return [False]
        
    try:
        prod = 1
        for i in range(1, p):
            inv = pow(i, -1, p)
            prod = (prod * inv) % p
            
        q_holds = (prod % p == (-1) % p)
        neg_q = not q_holds
    except ValueError:
        # ValueError is raised by pow() if an inverse does not exist,
        # meaning the product of inverses of ALL integers from 1 to p-1 is undefined.
        neg_q = True
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The product of the modular inverses of all integers from 1 to p-1 modulo p is not congruent to -1 (mod p)"
]

N_HYP = 0
NEG_Q_INDEX = 0