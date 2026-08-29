import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q = witness.get('q')
        else:
            n, q = witness
    except Exception:
        return [False, False]

    # H_1: n >= 1 is an integer coprime to q
    try:
        h1 = isinstance(n, int) and isinstance(q, int) and n >= 1 and math.gcd(n, q) == 1
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails.
    # The conclusion states that the splitting field of Phi_n(x) over F_q is F_{q^d}.
    # This implicitly requires F_q to be a valid finite field, meaning q must be a prime power.
    # If q is a prime power, the theorem is mathematically true.
    # If q is not a prime power, F_q is not a field, so the conclusion is false.
    try:
        if not isinstance(q, int) or q < 2:
            q_is_prime_power = False
        else:
            factors = sympy.ntheory.factorint(q)
            q_is_prime_power = (len(factors) == 1)
        
        neg_q = not q_is_prime_power
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer coprime to q",
    "¬Q: The conclusion fails (q is not a prime power, so F_q is not a field)"
]

N_HYP = 1
NEG_Q_INDEX = 1