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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def extract_xy(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            return witness[1], witness[2]
        elif len(witness) == 2:
            return witness[0], witness[1]
    raise ValueError("Witness must be a tuple of length 2 or 3")

def is_zero_expr(e):
    if e == 0:
        return True
    try:
        if e.is_zero:
            return True
    except AttributeError:
        pass
    try:
        return sympy.simplify(e) == 0
    except Exception:
        return False

def is_nilpotent(m):
    try:
        if hasattr(m, 'shape') and len(m.shape) == 2 and m.shape[0] == m.shape[1]:
            n = m.shape[0]
            if n == 0:
                return True
            mn = m**n
            return all(is_zero_expr(e) for e in mn)
        else:
            for i in range(1, 16):
                mi = m**i
                if hasattr(mi, '__iter__'):
                    if all(is_zero_expr(e) for e in mi):
                        return True
                else:
                    if is_zero_expr(mi):
                        return True
            return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: R is a ring
    try:
        x, y = extract_xy(witness)
        _ = x + y
        _ = x * y
        _ = y * x
        if hasattr(x, 'shape') and hasattr(y, 'shape'):
            h1_ok = (x.shape == y.shape and len(x.shape) == 2 and x.shape[0] == x.shape[1])
        else:
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: x and y are nilpotent elements of R
    try:
        x, y = extract_xy(witness)
        h2_ok = is_nilpotent(x) and is_nilpotent(y)
    except Exception:
        h2_ok = False

    # neg_Q: The sum x + y is NOT a nilpotent element of R
    try:
        x, y = extract_xy(witness)
        neg_q_ok = not is_nilpotent(x + y)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x and y are nilpotent elements of R",
    "¬Q: The sum x + y is not a nilpotent element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2