import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices.matrices import MatrixBase
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an n x n matrix with real entries
    try:
        h1 = isinstance(witness, MatrixBase) and witness.rows == witness.cols
        if h1:
            for i in range(witness.rows):
                for j in range(witness.cols):
                    if not witness[i, j].is_real:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: A is positive semidefinite iff all of its principal minors are non-negative is FALSE
    try:
        if not (isinstance(witness, MatrixBase) and witness.rows == witness.cols):
            neg_q = False
        else:
            n = witness.rows
            
            # Check if all principal minors of A are non-negative
            all_minors_nonneg = True
            for k in range(1, n + 1):
                for idx in itertools.combinations(range(n), k):
                    idx_list = list(idx)
                    sub_M = witness[idx_list, idx_list]
                    if sub_M.det() < 0:
                        all_minors_nonneg = False
                        break
                if not all_minors_nonneg:
                    break
                    
            # Check if A is positive semidefinite
            # A real matrix A is PSD iff its symmetric part (A + A^T)/2 is PSD.
            # A real symmetric matrix is PSD iff all of its principal minors are non-negative.
            sym_A = (witness + witness.T) / 2
            is_psd = True
            for k in range(1, n + 1):
                for idx in itertools.combinations(range(n), k):
                    idx_list = list(idx)
                    sub_M = sym_A[idx_list, idx_list]
                    if sub_M.det() < 0:
                        is_psd = False
                        break
                if not is_psd:
                    break
                    
            # The conclusion fails if the two conditions are not equivalent for the witness
            neg_q = (is_psd != all_minors_nonneg)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "¬Q: A is positive semidefinite XOR all of its principal minors are non-negative"
]

N_HYP = 1
NEG_Q_INDEX = 1