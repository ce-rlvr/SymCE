import sympy
from sympy.ntheory import is_primitive_root

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            p = witness['p']
        else:
            a, b, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(is_primitive_root(a, p))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_primitive_root(b, p))
    except Exception:
        h2 = False

    try:
        neg_q = bool(is_primitive_root(a * b, p))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is a primitive root modulo p",
    "H_2: b is a primitive root modulo p",
    "¬Q: ab is a primitive root modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2