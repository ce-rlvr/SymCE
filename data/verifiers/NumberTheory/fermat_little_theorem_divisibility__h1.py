import math
import itertools
import functools
import sympy

# Top-level setup
# (No named bindings needed for this number theory conjecture; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            p = witness.get('p')
        else:
            a, p = witness
    except Exception:
        return [False, False]

    try:
        a_int = int(a)
        # Check if a is mathematically an integer (handles int, sympy.Integer, and float like 2.0)
        h1 = (a == a_int) and not isinstance(a, bool)
    except Exception:
        h1 = False

    try:
        p_int = int(p)
        if p != p_int or p_int == 0 or isinstance(p, bool):
            neg_q = False
        elif p_int < 0:
            val = a_int**p_int - a_int
            if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
                neg_q = (int(val) % p_int != 0)
            else:
                # If a^p - a is not an integer, p cannot divide it
                neg_q = True
        else:
            # For p > 0, use modular exponentiation to avoid huge numbers
            rem = (pow(a_int, p_int, p_int) - (a_int % p_int)) % p_int
            neg_q = (rem != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: p does not divide a^p - a"
]

N_HYP = 1
NEG_Q_INDEX = 1