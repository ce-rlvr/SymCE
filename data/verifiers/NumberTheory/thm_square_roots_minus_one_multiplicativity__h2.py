import sympy
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def count_roots(k):
    if k == 1:
        return 1
    factors = factorint(k)
    ans = 1
    for p, e in factors.items():
        if p == 2:
            if e == 1:
                ans *= 1
            else:
                ans *= 0
        else:
            if p % 4 == 1:
                ans *= 2
            else:
                ans *= 0
    return ans

def conditions(witness):
    try:
        # Witness should be a tuple or list of two elements: (m, n)
        if len(witness) != 2:
            return [False, False]
        m, n = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = type(m) is int and type(n) is int and m > 0 and n > 0
    except Exception:
        h1_ok = False
        
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            roots_m = count_roots(m)
            roots_n = count_roots(n)
            roots_mn = count_roots(m * n)
            neg_q_ok = bool(roots_mn != roots_m * roots_n)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: The number of solutions to x^2 \\equiv -1 \\pmod{mn} is not the product of the number of solutions modulo m and modulo n"
]

N_HYP = 1
NEG_Q_INDEX = 1