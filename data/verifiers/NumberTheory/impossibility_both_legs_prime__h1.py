import sympy
from sympy.ntheory import isprime
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
        else:
            a, b, c = witness
    except Exception:
        return [False, False]

    try:
        lhs = sympy.sympify(a)**2 + sympy.sympify(b)**2
        rhs = sympy.sympify(c)**2
        diff = sympy.simplify(lhs - rhs)
        if diff == 0 or diff.is_zero:
            h1_ok = True
        else:
            try:
                h1_ok = bool(abs(float(diff)) < 1e-12)
            except Exception:
                h1_ok = False
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = bool(isprime(a) and isprime(b))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "¬Q: a and b are both prime numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1