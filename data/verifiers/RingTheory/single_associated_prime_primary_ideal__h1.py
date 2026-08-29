import sympy
from sympy import symbols
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

def get_bool_attr(obj, attrs):
    if isinstance(obj, dict):
        for attr in attrs:
            if attr in obj:
                return bool(obj[attr])
    else:
        for attr in attrs:
            if hasattr(obj, attr):
                return bool(getattr(obj, attr))
    raise AttributeError(f"Missing boolean attribute from {attrs}")

def get_list_attr(obj, attrs):
    if isinstance(obj, dict):
        for attr in attrs:
            if attr in obj:
                return list(obj[attr])
    else:
        for attr in attrs:
            if hasattr(obj, attr):
                return list(getattr(obj, attr))
    raise AttributeError(f"Missing list attribute from {attrs}")

def conditions(witness) -> list[bool]:
    # The witness can be an ideal I, or a tuple (R, I)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
    else:
        I = witness

    # H_1: I is a proper ideal of R
    try:
        h1 = get_bool_attr(I, ['is_proper_ideal', 'is_proper'])
    except Exception:
        h1 = False

    # ¬Q: The ideal I is a primary ideal if and only if the set of its associated prime ideals contains exactly one element.
    # Negation: I being primary is NOT equivalent to having exactly one associated prime.
    try:
        is_prim = get_bool_attr(I, ['is_primary_ideal', 'is_primary'])
        assoc = get_list_attr(I, ['associated_primes', 'assoc_primes', 'associated_prime_ideals'])
        has_one_assoc = (len(assoc) == 1)
        neg_q = (is_prim != has_one_assoc)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: I being primary is not equivalent to I having exactly one associated prime"
]

N_HYP = 1
NEG_Q_INDEX = 1