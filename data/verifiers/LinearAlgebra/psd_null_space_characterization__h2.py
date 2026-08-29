import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (A, x) where A is the matrix and x is the vector.
    """
    try:
        if len(witness) != 2:
            return [False, False]
        A_raw, x_raw = witness
        A = Matrix(A_raw)
        x = Matrix(x_raw)
    except Exception:
        return [False, False]

    # H_1: A is an n x n real positive semidefinite matrix and x is a compatible vector
    h1 = False
    try:
        if A.is_square and A.shape[0] == x.shape[0] and x.shape[1] == 1:
            if A == A.T and all(e.is_real for e in A):
                psd = None
                try:
                    psd = A.is_positive_semidefinite
                except Exception:
                    pass
                
                if psd is None:
                    evals = A.eigenvals()
                    psd = True
                    for e in evals:
                        if e.is_real and e < 0:
                            psd = False
                            break
                h1 = bool(psd)
    except Exception:
        h1 = False

    # ¬Q: x is not in the null space of A (Ax != 0)
    neg_q = False
    try:
        Ax = A * x
        if hasattr(Ax, 'is_zero_matrix') and Ax.is_zero_matrix is not None:
            neg_q = not Ax.is_zero_matrix
        else:
            neg_q = not all(sympy.simplify(e) == 0 for e in Ax)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real positive semidefinite matrix and x is a compatible vector",
    "¬Q: x is not in the null space of A (Ax != 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1