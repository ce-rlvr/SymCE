import sympy
from sympy.ntheory import n_order
import math
import itertools
import functools

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness can be a tuple (n, a) or (n, a, k).
    """
    try:
        witness = tuple(witness)
        if len(witness) == 3:
            n, a, k = witness
        elif len(witness) == 2:
            n, a = witness
            k = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n = 2^k
    try:
        n_int = int(n)
        if n != n_int:
            h1 = False
        elif k is not None:
            k_int = int(k)
            if k != k_int:
                h1 = False
            else:
                h1 = (n_int == 2**k_int)
        else:
            h1 = (n_int > 0 and (n_int & (n_int - 1)) == 0)
            if h1:
                k_int = n_int.bit_length() - 1
    except Exception:
        h1 = False

    # H_2: a is an odd integer
    try:
        a_int = int(a)
        if a != a_int:
            h2 = False
        else:
            h2 = (a_int % 2 != 0)
    except Exception:
        h2 = False

    # ¬Q: The multiplicative order of a modulo n is strictly greater than 2^{k-2}
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if n_int == 1:
                order = 1
            else:
                order = n_order(a_int, n_int)
            
            limit = 2**(k_int - 2)
            neg_q = bool(order > limit)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n = 2^k",
    "H_2: a is an odd integer",
    "¬Q: The multiplicative order of a modulo n is strictly greater than 2^{k-2}"
]

N_HYP = 2
NEG_Q_INDEX = 2