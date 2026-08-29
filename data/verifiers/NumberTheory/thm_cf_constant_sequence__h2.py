import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for Number Theory; use integers and sympy expressions directly)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should provide both `a` and `alpha`.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            alpha = witness.get('alpha')
        elif hasattr(witness, 'a') and hasattr(witness, 'alpha'):
            a = witness.a
            alpha = witness.alpha
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            a, alpha = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: a is a positive integer
    try:
        h1 = False
        if isinstance(a, (int, sympy.Integer)):
            h1 = bool(a > 0)
        elif isinstance(a, float) and a.is_integer():
            h1 = bool(a > 0)
        elif getattr(a, 'is_integer', False) and getattr(a, 'is_positive', False):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: alpha != (a + sqrt(a^2 + 4)) / 2
    try:
        expected_alpha = (a + sympy.sqrt(a**2 + 4)) / 2
        if isinstance(alpha, float) or getattr(alpha, 'is_Float', False):
            neg_q = abs(float(alpha) - float(expected_alpha)) > 1e-9
        else:
            diff = sympy.simplify(alpha - expected_alpha)
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is a positive integer",
    "¬Q: alpha != (a + sqrt(a^2 + 4)) / 2"
]

N_HYP = 1
NEG_Q_INDEX = 1