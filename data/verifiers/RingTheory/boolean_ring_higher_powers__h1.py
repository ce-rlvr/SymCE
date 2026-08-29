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

# Top-level setup for potential witness elements
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "H_2: x is an element of R",
    "¬Q: x^n != x"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Extract n and x from the witness
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            x = witness.get('x')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, n, x = witness
            elif len(witness) == 2:
                n, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Check H_1: n is an integer such that n >= 2
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and int(n) >= 2
    except Exception:
        h1 = False

    # Check H_2: x is an element of R
    # We verify this by checking if x supports basic ring multiplication
    try:
        _ = x * x
        h2 = True
    except Exception:
        h2 = False

    # Check ¬Q: x^n != x
    try:
        xn = x**n
        if hasattr(xn, 'equals') and callable(xn.equals):
            eq = xn.equals(x)
            if eq is None:
                diff = xn - x
                if hasattr(diff, 'simplify'):
                    diff = diff.simplify()
                if hasattr(diff, 'is_zero'):
                    neg_q = not diff.is_zero
                else:
                    neg_q = bool(diff != 0)
            else:
                neg_q = not eq
        elif hasattr(xn, 'decl') and hasattr(xn, 'sort'):
            # Handle z3 expressions
            neg_q = z3.is_true(z3.simplify(xn != x))
        else:
            neg_q = bool(xn != x)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]