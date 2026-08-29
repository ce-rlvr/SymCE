import sympy
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            k = witness['k']
        else:
            a, k = witness
    except Exception:
        return [False, False]

    # H_1: k >= 1 is an integer
    try:
        h1_ok = bool(isinstance(k, (int, sympy.Integer)) and not isinstance(k, bool) and k >= 1)
    except Exception:
        h1_ok = False

    # ¬Q: The modular inverse of 1-a modulo a^k is not congruent to sum_{i=0}^{k-1} a^i (mod a^k)
    try:
        modulus = a**k
        val = 1 - a
        
        # If the modular inverse cannot be computed (e.g., modulo 0), the conclusion fails.
        try:
            inv = sympy.mod_inverse(val, modulus)
        except Exception:
            q_ok = False
        else:
            sum_val = sum(a**i for i in range(k))
            q_ok = bool((inv - sum_val) % modulus == 0)
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: k >= 1 is an integer",
    "¬Q: The modular inverse of 1-a modulo a^k is not congruent to sum_{i=0}^{k-1} a^i (mod a^k)"
]

N_HYP = 1
NEG_Q_INDEX = 1