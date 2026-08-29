import sympy
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple (p, g)
        p, g = witness
        p = int(p)
        g = int(g)
    except Exception:
        return [False, False]

    # H_1: p is a prime number congruent to 1 modulo 4
    try:
        h1_ok = bool(sympy.ntheory.isprime(p) and p % 4 == 1)
    except Exception:
        h1_ok = False

    # ¬Q: -g is NOT a primitive root modulo p
    try:
        neg_q_ok = not bool(sympy.ntheory.is_primitive_root(-g, p))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number congruent to 1 modulo 4",
    "¬Q: -g is not a primitive root modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1