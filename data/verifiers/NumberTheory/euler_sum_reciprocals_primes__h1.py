import sympy
from sympy.ntheory import isprime
import math
import itertools
import functools

def conditions(witness):
    try:
        count = 0
        for p in witness:
            if not isinstance(p, (int, sympy.Integer)) or not isprime(p):
                return [False]
            count += 1
            if count > 10000:
                # If the iterable is too large or infinite, we cannot easily verify convergence
                return [False]
        # A finite set of primes has a finite sum of reciprocals, which trivially converges.
        # Thus, the conclusion that the series diverges is FALSE.
        neg_q = True
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: The sum of reciprocals of P converges (e.g., P is a finite set of primes)"]
N_HYP = 0
NEG_Q_INDEX = 0