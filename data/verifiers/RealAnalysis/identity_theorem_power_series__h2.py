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
x, y, z, c = sympy.symbols('x y z c')

def conditions(witness):
    """
    witness: tuple representing the two power series.
    Can be (a, b), (a, b, R1, R2), or (a, b, c, R1, R2)
    where a and b are lists/tuples of coefficients or callables.
    """
    h1_ok = False
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
                if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                    h1_ok = True
                elif callable(a) and callable(b):
                    h1_ok = True
            elif len(witness) == 4:
                a, b, R1, R2 = witness
                if R1 > 0 and R2 > 0:
                    h1_ok = True
            elif len(witness) >= 5:
                a, b, c_val, R1, R2 = witness[:5]
                if R1 > 0 and R2 > 0:
                    h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
            elif len(witness) == 4:
                a, b, R1, R2 = witness
            elif len(witness) >= 5:
                a, b, c_val, R1, R2 = witness[:5]
            else:
                a, b = None, None
                
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                max_len = max(len(a), len(b))
                identical = True
                for n in range(max_len):
                    val_a = a[n] if n < len(a) else 0
                    val_b = b[n] if n < len(b) else 0
                    try:
                        diff = val_a - val_b
                        if isinstance(diff, sympy.Expr):
                            if diff.simplify() != 0:
                                identical = False
                                break
                        elif diff != 0:
                            identical = False
                            break
                    except Exception:
                        if val_a != val_b:
                            identical = False
                            break
                neg_q_ok = not identical
            elif callable(a) and callable(b):
                identical = True
                for n in range(100):
                    val_a = a(n)
                    val_b = b(n)
                    try:
                        diff = val_a - val_b
                        if isinstance(diff, sympy.Expr):
                            if diff.simplify() != 0:
                                identical = False
                                break
                        elif diff != 0:
                            identical = False
                            break
                    except Exception:
                        if val_a != val_b:
                            identical = False
                            break
                neg_q_ok = not identical
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a_n and b_n are power series with radii of convergence R_1 > 0 and R_2 > 0",
    "¬Q: The coefficients are not identical (there exists n such that a_n != b_n)"
]

N_HYP = 1
NEG_Q_INDEX = 1