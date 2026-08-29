import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Check the remaining hypotheses and the negated conclusion for the given witness.
    The witness should provide both 'n' and 'k'.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            k = witness['k']
        elif hasattr(witness, 'n') and hasattr(witness, 'k'):
            n = witness.n
            k = witness.k
        else:
            n, k = witness
    except Exception:
        return [False, False]

    # H_1: k is a non-negative integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and int(k) >= 0
    except Exception:
        h1 = False

    # ¬Q: sigma(n) != 2^{k+1} - 1
    try:
        if isinstance(n, (int, sympy.Integer)) and int(n) >= 1:
            neg_q = sympy.divisor_sigma(int(n)) != (2**(int(k) + 1) - 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k is a non-negative integer",
    "¬Q: sigma(n) != 2^{k+1} - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1