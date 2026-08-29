import sympy
import math
import itertools
import functools

# Top-level setup
# No named bindings needed for this Number Theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness can be a dictionary with keys 'a', 'b', 'c', 'd', 'm' 
    or a tuple in the order (a, b, c, d, m).
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
            m = witness['m']
        else:
            a, b, c, d, m = witness
    except Exception:
        return [False, False, False]

    # H_1: a \equiv b \pmod m
    try:
        h1_ok = bool((a - b) % m == 0)
    except Exception:
        h1_ok = False

    # H_2: c \equiv d \pmod m
    try:
        h2_ok = bool((c - d) % m == 0)
    except Exception:
        h2_ok = False

    # ¬Q: a + c \not\equiv b + d \pmod m
    try:
        neg_q_ok = bool(((a + c) - (b + d)) % m != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a \\equiv b \\pmod m",
    "H_2: c \\equiv d \\pmod m",
    "¬Q: a + c \\not\\equiv b + d \\pmod m"
]

N_HYP = 2
NEG_Q_INDEX = 2