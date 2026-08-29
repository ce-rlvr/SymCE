import sympy
import sympy.ntheory
import math
import itertools
import functools

def conditions(witness):
    try:
        if type(witness) is bool:
            h1 = False
        elif not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n > 0)
    except Exception:
        h1 = False

    try:
        if type(witness) is bool:
            neg_q = False
        elif not isinstance(witness, (int, sympy.Integer)):
            neg_q = False
        else:
            n = int(witness)
            if n <= 0:
                neg_q = False
            elif n == 1:
                # Z/1Z is the zero ring, which is the empty direct product of finite fields.
                neg_q = False
            else:
                # Z/nZ is isomorphic to a direct product of finite fields if and only if
                # n is square-free (i.e., no prime factor has multiplicity > 1).
                # Thus, the conclusion FAILS (neg_q is True) iff n is NOT square-free.
                factors = sympy.ntheory.factorint(n)
                neg_q = any(v > 1 for v in factors.values())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: Z/nZ is not isomorphic to a direct product of finite fields"
]

N_HYP = 1
NEG_Q_INDEX = 1