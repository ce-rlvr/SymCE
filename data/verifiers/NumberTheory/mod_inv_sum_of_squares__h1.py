import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        p = sympy.S(witness)
        if not p.is_integer:
            h1_ok = False
        else:
            h1_ok = bool(p > 3)
    except Exception:
        h1_ok = False

    try:
        p = sympy.S(witness)
        if not p.is_integer:
            q_holds = False
        else:
            p_int = int(p)
            total = 0
            for i in range(1, p_int):
                inv = sympy.mod_inverse(i, p_int)
                total += inv**2
            q_holds = bool(total % p_int == 0)
    except Exception:
        # If an inverse does not exist, the sum cannot be computed,
        # so the statement that the sum is congruent to 0 mod p is false.
        q_holds = False

    neg_q_ok = not q_holds

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p > 3",
    "¬Q: The sum of the squares of the modular inverses of the integers from 1 to p-1 modulo p is not congruent to 0 (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1