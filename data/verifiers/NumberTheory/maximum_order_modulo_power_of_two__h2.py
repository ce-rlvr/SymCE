import sympy
from sympy.ntheory import n_order
import math
import itertools
import functools

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness):
    try:
        a, k = witness
    except Exception:
        return [False, False]
        
    try:
        k_int = int(k)
        h1 = (k_int == k) and (k_int > 2)
    except Exception:
        h1 = False
        
    try:
        a_int = int(a)
        k_int = int(k)
        if k_int < 2:
            neg_q = False
        else:
            try:
                order = n_order(a_int, 2**k_int)
                neg_q = (2**(k_int - 2)) % order != 0
            except ValueError:
                # n_order raises ValueError if gcd(a, 2^k) != 1.
                # In this case, the multiplicative order is undefined,
                # so it does not divide 2^{k-2}.
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer strictly greater than 2",
    "¬Q: The multiplicative order of a modulo 2^k does not divide 2^{k-2}"
]

N_HYP = 1
NEG_Q_INDEX = 1