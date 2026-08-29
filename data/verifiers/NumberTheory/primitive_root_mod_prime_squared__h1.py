import sympy
from sympy.ntheory import is_primitive_root
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            g = int(witness['g'])
            p = int(witness['p'])
        else:
            g = int(witness[0])
            p = int(witness[1])
    except Exception:
        return [False, False]

    try:
        h1 = bool(is_primitive_root(g, p))
    except Exception:
        h1 = False

    try:
        neg_q = (not bool(is_primitive_root(g, p**2))) and (not bool(is_primitive_root(g + p, p**2)))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: g is a primitive root modulo p",
    "¬Q: Neither g nor g+p is a primitive root modulo p^2"
]

N_HYP = 1
NEG_Q_INDEX = 1