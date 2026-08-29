import sympy
from sympy.ntheory import divisor_count
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (int, sympy.Integer)) and isinstance(witness[1], (list, tuple)):
            n, exponents = witness
            h1 = bool(n > 1)
        else:
            if isinstance(witness, dict):
                items = witness.items()
            else:
                items = witness
            n = 1
            for base, exp in items:
                if not isinstance(base, (int, sympy.Integer)) or not isinstance(exp, (int, sympy.Integer)):
                    raise ValueError
                n *= base ** exp
            h1 = bool(n > 1)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (int, sympy.Integer)) and isinstance(witness[1], (list, tuple)):
            n, exponents = witness
            formula_tau = 1
            for exp in exponents:
                formula_tau *= (exp + 1)
        else:
            if isinstance(witness, dict):
                items = witness.items()
            else:
                items = witness
            n = 1
            formula_tau = 1
            for base, exp in items:
                n *= base ** exp
                formula_tau *= (exp + 1)
                
        actual_tau = divisor_count(n)
        neg_q = bool(actual_tau != formula_tau)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer strictly greater than 1",
    "¬Q: tau(n) is not equal to (a_1 + 1)(a_2 + 1)...(a_k + 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1