import sympy
from sympy import eye, zeros, Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Check if witness is a matrix
    try:
        if not getattr(witness, 'is_Matrix', False):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: The entries of Q are real numbers
    try:
        h1 = all(sympy.sympify(e).is_real == True for e in witness)
    except Exception:
        h1 = False

    # H_2: Q is an orthogonal matrix
    # A matrix is considered orthogonal if its columns are orthonormal or its rows are orthonormal.
    try:
        diff1 = sympy.simplify(witness.T * witness - eye(witness.cols))
        diff2 = sympy.simplify(witness * witness.T - eye(witness.rows))
        h2 = (diff1 == zeros(witness.cols, witness.cols)) or (diff2 == zeros(witness.rows, witness.rows))
    except Exception:
        h2 = False

    # ¬Q: Q is not invertible or its inverse is not an orthogonal matrix
    try:
        if not witness.is_square:
            neg_q = True
        else:
            try:
                inv_Q = witness.inv()
                diff_inv1 = sympy.simplify(inv_Q.T * inv_Q - eye(inv_Q.cols))
                diff_inv2 = sympy.simplify(inv_Q * inv_Q.T - eye(inv_Q.rows))
                inv_ortho = (diff_inv1 == zeros(inv_Q.cols, inv_Q.cols)) or (diff_inv2 == zeros(inv_Q.rows, inv_Q.rows))
                neg_q = not inv_ortho
            except Exception:
                # If it's square but not invertible (e.g., determinant is 0)
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The entries of Q are real numbers",
    "H_2: Q is an orthogonal matrix",
    "¬Q: Q is not invertible or its inverse is not an orthogonal matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2