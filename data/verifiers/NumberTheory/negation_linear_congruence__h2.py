import sympy
import math
import itertools
import functools

# Top-level setup
# No special named bindings needed for Number Theory; integers are used directly.

def is_integer(x):
    if isinstance(x, bool):
        return False
    if isinstance(x, int):
        return True
    if isinstance(x, sympy.Integer):
        return True
    if hasattr(x, 'is_integer'):
        if callable(x.is_integer):
            try:
                return x.is_integer()
            except Exception:
                pass
        else:
            return bool(x.is_integer)
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            m = witness.get('m')
        else:
            a, b, m = witness
    except Exception:
        return [False, False, False]

    # H_1: a and b are integers
    try:
        h1 = is_integer(a) and is_integer(b)
    except Exception:
        h1 = False

    # H_2: a \equiv b \pmod m
    try:
        if m == 0:
            h2 = (a == b)
        else:
            h2 = ((a - b) % m == 0)
    except Exception:
        h2 = False

    # \neg Q: -a \not\equiv -b \pmod m
    try:
        if m == 0:
            q = (-a == -b)
        else:
            q = ((-a - (-b)) % m == 0)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "H_2: a \\equiv b \\pmod m",
    "¬Q: -a \\not\\equiv -b \\pmod m"
]

N_HYP = 2
NEG_Q_INDEX = 2