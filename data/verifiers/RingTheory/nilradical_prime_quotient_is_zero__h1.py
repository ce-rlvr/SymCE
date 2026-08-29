import sympy
import sympy.abc
from sympy.matrices import eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_prime_ideal'):
            h1 = bool(witness.is_prime_ideal())
        elif isinstance(witness, dict):
            h1 = bool(witness.get('is_prime_ideal', False))
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'nilradical_of_quotient_is_zero'):
            q = bool(witness.nilradical_of_quotient_is_zero())
        elif isinstance(witness, dict):
            q = bool(witness.get('nilradical_of_quotient_is_zero', True))
        else:
            q = True
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: The nilradical of the quotient ring R/P is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1