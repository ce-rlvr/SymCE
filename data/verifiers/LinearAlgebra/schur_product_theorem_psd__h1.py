import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
            
        if not (hasattr(A, 'is_Matrix') and A.is_Matrix):
            A = Matrix(A)
        if not (hasattr(B, 'is_Matrix') and B.is_Matrix):
            B = Matrix(B)
    except Exception:
        return [False, False]

    def is_psd(M):
        try:
            if not hasattr(M, 'is_square') or not M.is_square:
                return False
            if not M.is_symmetric():
                return False
            for e in M:
                if hasattr(e, 'is_real') and e.is_real is False:
                    return False
            evs = M.eigenvals()
            for ev in evs:
                if hasattr(ev, 'is_real') and ev.is_real is False:
                    return False
                try:
                    val = float(ev.evalf())
                    if val < -1e-9:
                        return False
                except Exception:
                    try:
                        if bool(ev < 0):
                            return False
                    except Exception:
                        return False
            return True
        except Exception:
            return False

    # H1: B is a real n x n positive semidefinite matrix
    try:
        h1 = is_psd(B)
    except Exception:
        h1 = False

    # neg_Q: A \circ B is NOT a positive semidefinite matrix
    try:
        if not hasattr(A, 'shape') or not hasattr(B, 'shape') or A.shape != B.shape:
            neg_q = False
        else:
            C = Matrix(A.rows, A.cols, lambda i, j: A[i, j] * B[i, j])
            neg_q = not is_psd(C)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is a real n x n positive semidefinite matrix",
    "¬Q: The Hadamard product A \\circ B is not a positive semidefinite matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1