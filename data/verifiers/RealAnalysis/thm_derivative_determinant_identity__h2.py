import sympy
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # Extract H if witness is provided as a tuple (n, H)
    if isinstance(witness, tuple) and len(witness) == 2:
        _, H_wit = witness
    else:
        H_wit = witness

    # H_1: Witness is a matrix
    try:
        if isinstance(H_wit, list) and all(isinstance(row, list) for row in H_wit):
            H = sympy.Matrix(H_wit)
        else:
            H = H_wit
        h1 = isinstance(H, sympy.MatrixBase)
    except Exception:
        h1 = False
        H = H_wit

    # H_2: Witness has real entries
    try:
        if h1:
            h2 = all(e.is_real for e in H)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The total derivative of det at I evaluated at H is not equal to the trace of H
    # (This fails, for instance, if H is not a square matrix, making the evaluation undefined)
    try:
        if not h1:
            neg_q = False
        elif not H.is_square:
            neg_q = True
        else:
            n = H.shape[0]
            I = sympy.eye(n)
            t = sympy.Symbol('t')
            poly = (I + t * H).det()
            deriv = sympy.diff(poly, t).subs(t, 0)
            neg_q = bool(sympy.simplify(deriv - H.trace()) != 0)
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Witness is a matrix",
    "H_2: Witness has real entries",
    "¬Q: The total derivative of det at I evaluated at H is not equal to the trace of H (or is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2