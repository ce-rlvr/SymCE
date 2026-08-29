import sympy
from sympy import eye, zeros, Matrix
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            x, y = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a ring
    try:
        _ = x + y
        _ = x * y
        _ = y * x
        _ = x - y
        h1 = bool(x + y == y + x)
    except Exception:
        h1 = False

    # H2: x and y commute
    try:
        h2 = bool(x * y == y * x)
    except Exception:
        h2 = False

    # neg_Q: x + y is NOT nilpotent
    try:
        z = x + y
        is_nilp = False
        
        if hasattr(z, 'is_nilpotent'):
            try:
                res = z.is_nilpotent()
                if res is not None:
                    is_nilp = bool(res)
            except Exception:
                pass
        
        if not is_nilp:
            if hasattr(z, 'shape') and len(z.shape) == 2 and z.shape[0] == z.shape[1]:
                n = z.shape[0]
                zero_mat = z * 0
                is_nilp = bool(z**n == zero_mat)
            else:
                if z == z * 0:
                    is_nilp = True
                else:
                    curr = z
                    for _ in range(100):
                        curr = curr * z
                        if curr == z * 0:
                            is_nilp = True
                            break
        
        neg_q = not is_nilp
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x and y commute",
    "¬Q: x + y is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2