import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
import math
import itertools
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, S, e, f = witness
            elif len(witness) == 2:
                e, f = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def apply_f(func, val):
        if callable(func):
            return func(val)
        elif isinstance(func, dict):
            return func[val]
        elif isinstance(func, (list, tuple)):
            for k, v in func:
                if k == val:
                    return v
        raise ValueError("f is not callable, dict, or list of pairs")

    # H_1: R and S are rings
    # We verify this by checking if e and f(e) support basic ring operations (+, -, *)
    try:
        fe = apply_f(f, e)
        _ = e + e
        _ = e - e
        _ = e * e
        _ = fe + fe
        _ = fe - fe
        _ = fe * fe
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: e in R is an idempotent element, meaning e^2 = e
    try:
        h2_ok = bool(e * e == e)
    except Exception:
        h2_ok = False

    # ¬Q: f(e) is NOT an idempotent element in S
    try:
        fe = apply_f(f, e)
        neg_q_ok = bool(fe * fe != fe)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: e in R is an idempotent element",
    "¬Q: f(e) is not an idempotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2