import sympy
from sympy import eye, zeros, I

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a symmetric matrix",
    "¬Q: There does not exist an orthogonal matrix P such that P^T A P is diagonal"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: A is a symmetric matrix
    try:
        if callable(witness.is_symmetric):
            h1 = witness.is_symmetric()
        else:
            h1 = witness.is_symmetric
            
        if h1 is None:
            h1 = False
        else:
            h1 = bool(h1)
    except Exception:
        try:
            h1 = bool(witness == witness.T)
        except Exception:
            h1 = False

    # ¬Q: A is not orthogonally diagonalizable
    try:
        # Check if the matrix is square
        is_sq = (witness.shape[0] == witness.shape[1])
        if not is_sq:
            neg_q = True
        else:
            # For a symmetric matrix over the complex numbers, it is orthogonally 
            # diagonalizable if and only if it is diagonalizable.
            # The standard counterexample (e.g., [[1, I], [I, -1]]) is not diagonalizable.
            if callable(witness.is_diagonalizable):
                diag = witness.is_diagonalizable()
            else:
                diag = witness.is_diagonalizable
                
            if diag is None:
                neg_q = False
            else:
                neg_q = not bool(diag)
    except Exception:
        neg_q = False

    return [h1, neg_q]