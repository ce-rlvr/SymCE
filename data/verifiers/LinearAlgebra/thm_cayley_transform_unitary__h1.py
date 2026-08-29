import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # H_1: H is a square matrix
    try:
        if not isinstance(witness, sympy.MatrixBase):
            H_mat = sympy.Matrix(witness)
        else:
            H_mat = witness
        h1_ok = H_mat.is_square
    except Exception:
        h1_ok = False
        H_mat = None

    # ¬Q: The matrix (I - iH)(I + iH)^{-1} is not a unitary matrix
    try:
        if not h1_ok or H_mat is None:
            neg_q_ok = False
        else:
            n = H_mat.rows
            I_mat = sympy.eye(n)
            i = sympy.I
            A = I_mat + i * H_mat
            
            def is_zero(val):
                try:
                    val = sympy.simplify(val)
                except Exception:
                    pass
                if val == 0 or getattr(val, 'is_zero', False):
                    return True
                try:
                    num = complex(val.evalf())
                    if abs(num) < 1e-9:
                        return True
                except Exception:
                    pass
                return False

            # If (I + iH) is not invertible, the expression is undefined, hence not a unitary matrix.
            if is_zero(A.det()):
                neg_q_ok = True
            else:
                try:
                    A_inv = A.inv()
                except Exception:
                    neg_q_ok = True
                else:
                    B = I_mat - i * H_mat
                    U = B * A_inv
                    # A matrix U is unitary if U * U^H = I
                    diff = U * U.adjoint() - I_mat
                    # If not all elements of the difference are zero, it is not unitary
                    neg_q_ok = not all(is_zero(val) for val in diff)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a square matrix",
    "¬Q: The matrix (I - iH)(I + iH)^{-1} is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1