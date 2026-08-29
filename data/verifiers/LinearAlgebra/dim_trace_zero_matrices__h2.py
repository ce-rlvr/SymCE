import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_matrix(obj):
    """Check if an object is a matrix-like object with a 2D shape and tolist method."""
    return hasattr(obj, 'shape') and isinstance(obj.shape, tuple) and len(obj.shape) == 2 and hasattr(obj, 'tolist')

def conditions(witness) -> list[bool]:
    # H_1: S is a subset of n x n matrices (representing a subspace)
    try:
        n_val = None
        w = None
        
        # Parse witness: could be (n, S), a single matrix, or a collection of matrices
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n_val, S_val = witness
            if is_matrix(S_val):
                w = [S_val]
            elif isinstance(S_val, (list, tuple, set)):
                w = list(S_val)
        elif is_matrix(witness):
            w = [witness]
        elif isinstance(witness, (list, tuple, set)):
            w = list(witness)

        if w is None:
            h1 = False
        else:
            n = n_val
            h1 = True
            for m in w:
                if not is_matrix(m):
                    h1 = False
                    break
                if m.shape[0] != m.shape[1]:
                    h1 = False
                    break
                if n is None:
                    n = m.shape[0]
                elif n != m.shape[0]:
                    h1 = False
                    break
            if n is None or n < 1:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: S does not have dimension n^2 - 1
    try:
        if not h1:
            neg_q = False
        else:
            if len(w) == 0:
                dim = 0
            else:
                # Flatten each matrix into a row vector and find the rank of the resulting matrix
                # This gives the dimension of the subspace spanned by the matrices in S
                M = sympy.Matrix([list(m) for m in w])
                dim = M.rank()
            neg_q = bool(dim != n**2 - 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is a subset of n x n matrices",
    "¬Q: S does not have dimension n^2 - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1