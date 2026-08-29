import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, dict):
            u_wit = witness.get('u')
            v_wit = witness.get('v')
            if u_wit is None or v_wit is None:
                return [False, False, False]
            A_provided = 'A' in witness
            if A_provided:
                A_wit_raw = witness['A']
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                u_wit, v_wit = witness
                A_provided = False
            elif len(witness) == 3:
                u_wit, v_wit, A_wit_raw = witness
                A_provided = True
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        try:
            u = Matrix(u_wit)
            v = Matrix(v_wit)
        except Exception:
            return [False, False, False]

        # H_1: u and v are non-zero n x 1 column vectors
        h1 = False
        if u.shape[1] == 1 and v.shape[1] == 1:
            if u.shape[0] == v.shape[0] and u.shape[0] >= 1:
                u_is_zero = all(val == 0 for val in u)
                v_is_zero = all(val == 0 for val in v)
                if not u_is_zero and not v_is_zero:
                    h1 = True

        # H_2: A is the n x n matrix defined as A = I + u v^T
        h2 = False
        A_wit = None
        if h1:
            n = u.shape[0]
            A_calc = eye(n) + u * v.T
            if A_provided:
                try:
                    A_wit = Matrix(A_wit_raw)
                    if A_wit == A_calc or A_wit.equals(A_calc):
                        h2 = True
                except Exception:
                    h2 = False
            else:
                h2 = True
                A_wit = A_calc

        # ¬Q: A is not diagonalizable
        neg_q = False
        if h1 and h2 and A_wit is not None:
            try:
                # is_diagonalizable returns True if diagonalizable, False if not.
                # We want the negated conclusion (i.e., it is NOT diagonalizable).
                neg_q = (A_wit.is_diagonalizable() == False)
            except Exception:
                neg_q = False

        return [h1, h2, neg_q]

    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: u and v are non-zero n x 1 column vectors",
    "H_2: A is the n x n matrix defined as A = I + u v^T",
    "¬Q: A is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2