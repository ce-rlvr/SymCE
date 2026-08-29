import sympy
import sympy.ntheory
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            p = witness.get('p')
        else:
            a, p = witness
        a = int(a)
        p = int(p)
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 == 1)
    except Exception:
        h1 = False

    # H_2: The order of a modulo p is an odd integer
    try:
        order = sympy.n_order(a, p)
        h2 = bool(order % 2 == 1)
    except Exception:
        h2 = False

    # ¬Q: The integer a is not a quadratic residue modulo p
    try:
        a_mod = a % p
        if a_mod == 0:
            is_residue = True
        elif sympy.isprime(p):
            is_residue = pow(a_mod, (p - 1) // 2, p) == 1
        else:
            if p < 100000:
                is_residue = any((x * x) % p == a_mod for x in range(p))
            else:
                is_residue = False
        neg_q = not is_residue
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: The order of a modulo p is an odd integer",
    "¬Q: The integer a is not a quadratic residue modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2